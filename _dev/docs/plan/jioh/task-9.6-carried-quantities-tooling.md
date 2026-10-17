# 9.6 carried-quantities tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The build campaign's analysis and pooling compute every value the 9.6 fold-in carries (D16, D19–D22) and evaluate the extended stability criterion on them (D23, D24), so the top-up loop can decide after each repeat.

**Architecture:** A new module `dataset/tools/meas/build/shapes.py` holds the pure readings (runs between voluntary blocks, program-level gaps, share past the boot slice, `tracker`'s job end, object-job member steps). `analyze.py` calls it per repeat and returns the samples; `pool.py` pools them into quantile tables and evaluates the criterion through the shared `stability.py`, which gains an absolute floor and a minimum repeat count without changing its default behaviour (9.5 uses it).

**Tech Stack:** Python 3.12 (standard library only), pytest.

**Spec:** `_dev/research/jioh/task-9.6-compile/changelog.md` D16, D19–D24; `_dev/research/jioh/task-9.6-compile/campaign/method.md` §8, the four 2026-09-19 entries.

## Global Constraints

- Branch `jioh/dataset-rebuild`; the working tree is shared with another session — stage by explicit path only.
- Commit form: `<type>(jioh/phase-9): …`.
- `dataset/tools/meas/stability.py` is shared with 9.5 (9.5 D26): called without the new arguments it must return exactly what it returns today.
- Do not touch 9.5 files (`dataset/tools/meas/campaign/`, `_dev/research/jioh/task-9.5-*`) or the 9.5 items of `_dev/TODO.md`.
- Tests: `python3.12 -m pytest dataset/tools/tests/<file> -q` from the repository root.
- Raw records of the four pooled repeats: `~/.cache/meas-loop/pool/build-build-from10/meas-build-r{4,5,7,8}-full/`.
- Boot slice 10 000 µs (`docs/recognition-vocabulary.md` §2); trace resolution 1 µs; tolerance max(5 % of the mean, 1 µs); minimum five repeats.

## File Structure

- Create `dataset/tools/meas/build/shapes.py` — the D16/D20–D22 readings, pure functions over `analyze.Seg`.
- Modify `dataset/tools/meas/stability.py` — `abs_floor`, `min_k`, `half_width_abs`.
- Modify `dataset/tools/meas/build/analyze.py` — import `shapes`; `tracker` program gains `gst-plugin-scan`; `load_edges` keeps the real clock; `batch()` gains the job window and shape samples; make phases gain `object_members`; `main()` strips and prints the new fields.
- Modify `dataset/tools/meas/build/pool.py` — pools `object_members` and batch shapes, `criterion(out)` per D23/D24, `--title`, results sections.
- Create `dataset/tools/tests/test_meas_build.py` — tests for the above.
- Regenerate `_dev/research/jioh/task-9.6-compile/campaign/results.md` and `campaign/results/pooled.json`.

---

### Task 1: `stability()` gains an absolute floor and a minimum repeat count

**Files:**
- Modify: `dataset/tools/meas/stability.py`
- Test: `dataset/tools/tests/test_meas_build.py` (create)

**Interfaces:**
- Produces: `stability(values_by_repeat, abs_floor=None, min_k=None) -> dict` with keys `k, mean, cv, half_width, half_width_abs, leave_one_out, passes`.

- [ ] **Step 1: Write the failing tests**

Create `dataset/tools/tests/test_meas_build.py`:

```python
"""The 9.6 build campaign's carried quantities (changelog D16, D19–D24)."""

import pytest

from meas import stability as stab


def test_stability_default_is_unchanged():
    r = stab.stability({4: 360.0, 5: 372.0, 7: 365.0, 8: 369.0})
    assert r["k"] == 4 and r["passes"] is True
    assert r["half_width"] == pytest.approx(3.182 * 27 ** 0.5 / 2 / 366.5, abs=1e-4)
    assert "half_width_abs" in r


def test_abs_floor_passes_medians_at_the_trace_resolution():
    vals = [7.0, 7.0, 6.0, 6.0]          # µs: a one-step flip is 14 % of the mean
    assert stab.stability(vals)["passes"] is False
    r = stab.stability(vals, abs_floor=1.0)
    assert r["half_width_abs"] == pytest.approx(0.9186, abs=1e-3) and r["passes"] is True


def test_min_k_holds_the_criterion_back_below_five_repeats():
    vals = [100.0, 101.0, 100.5, 100.2]
    assert stab.stability(vals)["passes"] is True
    assert stab.stability(vals, min_k=5)["passes"] is False
    assert stab.stability(vals + [100.4], min_k=5)["passes"] is True
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q`
Expected: FAIL — `half_width_abs` missing; `stability()` got an unexpected keyword argument `abs_floor`.

- [ ] **Step 3: Implement**

Replace the body of `dataset/tools/meas/stability.py` from `def stability` to the end with:

```python
def stability(values_by_repeat, abs_floor=None, min_k=None):
    """The half-width of one carried median over its repeats (a dict keyed by repeat, or a list), and the largest
    shift of the mean when any one repeat is dropped. abs_floor (in the values' unit): the tolerance is the larger of
    TOLERANCE × mean and abs_floor, the instrument's resolution (9.6 changelog D23: the trace's 1 µs). min_k: the
    criterion holds only over at least that many repeats (9.6 changelog D24; kalibera-ismm13 §11). Without them the
    rule is the one 9.5 D26 and 9.6 D11 stated."""
    vals = values_by_repeat.values() if isinstance(values_by_repeat, dict) else values_by_repeat
    v = [x for x in vals if x]
    k = len(v)
    if k < 2:
        return {"k": k, "mean": v[0] if v else None, "cv": None, "half_width": None, "half_width_abs": None,
                "leave_one_out": None, "passes": False}
    m, sd = statistics.fmean(v), statistics.stdev(v)
    hw_abs = T975.get(k, T975[20]) * sd / (k ** 0.5)
    hw = hw_abs / m
    loo = max(abs(statistics.fmean(v[:i] + v[i + 1:]) - m) / m for i in range(k))
    ok = hw <= TOLERANCE if abs_floor is None else hw_abs <= max(TOLERANCE * m, abs_floor)
    if min_k is not None and k < min_k:
        ok = False
    return {"k": k, "mean": round(m, 4), "cv": round(sd / m, 4), "half_width": round(hw, 4),
            "half_width_abs": round(hw_abs, 4), "leave_one_out": round(loo, 4), "passes": ok}
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py dataset/tools/tests/test_meas.py -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add dataset/tools/meas/stability.py dataset/tools/tests/test_meas_build.py
git commit -m "feat(jioh/phase-9): 9.6 D23–D24 stability rule — absolute floor and minimum repeats, defaults unchanged for 9.5"
```

---

### Task 2: `shapes.py` — runs between blocks, share past the slice, program-level gaps

**Files:**
- Create: `dataset/tools/meas/build/shapes.py`
- Test: `dataset/tools/tests/test_meas_build.py`

**Interfaces:**
- Consumes: `analyze.Seg` (`t_in t_wake t_end run comm tid pid state cpu`; times s, run ms).
- Produces: `runs_between_blocks(rows) -> list[float]` (ms); `share_past_slice(runs_ms, slice_ms=BOOT_SLICE_MS) -> float | None`; `program_gaps(rows, start, end) -> list[float]` (ms); constants `BOOT_SLICE_MS = 10.0`, `VOLUNTARY`, `OBJECT_MEMBERS`, `STATUS`.

- [ ] **Step 1: Write the failing tests**

Append to `dataset/tools/tests/test_meas_build.py`:

```python
from meas.build import analyze as build
from meas.build import shapes


def seg(t_in, run_ms, tid, state, delay_ms=0.0):
    return build.Seg(t_in, t_in - delay_ms / 1000, t_in + run_ms / 1000, run_ms, "p", tid, 1, state, 3)


def test_runs_between_blocks_sum_across_preemptions_and_end_at_exit():
    rows = [seg(1.000, 4.0, 7, "R"), seg(1.005, 1.0, 8, "S"), seg(1.010, 3.0, 7, "S"),
            seg(1.020, 2.0, 7, "D"), seg(1.030, 5.0, 7, "Z")]
    assert sorted(shapes.runs_between_blocks(rows)) == pytest.approx([1.0, 2.0, 5.0, 7.0])


def test_share_past_slice():
    assert shapes.share_past_slice([12.0, 8.0, 30.0], 10.0) == pytest.approx(22.0 / 50.0)
    assert shapes.share_past_slice([]) is None


def test_program_gaps_count_runnable_time_as_busy():
    rows = [build.Seg(1.000, 1.000, 1.004, 4.0, "p", 7, 1, "S", 3),
            build.Seg(1.004, 1.003, 1.006, 2.0, "p", 8, 1, "R", 3),    # preempted at 1.006
            build.Seg(1.009, 1.009, 1.010, 1.0, "p", 8, 1, "S", 3),    # back at 1.009 with no reported delay
            build.Seg(1.015, 1.015, 1.016, 1.0, "p", 7, 1, "Z", 3)]
    assert shapes.program_gaps(rows, 1.000, 1.016) == pytest.approx([5.0])
    assert shapes.program_gaps(rows, 1.000, 1.020) == pytest.approx([5.0, 4.0])
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q`
Expected: FAIL — `ImportError: cannot import name 'shapes' from 'meas.build'`.

- [ ] **Step 3: Implement**

Create `dataset/tools/meas/build/shapes.py`:

```python
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
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add dataset/tools/meas/build/shapes.py dataset/tools/tests/test_meas_build.py
git commit -m "feat(jioh/phase-9): 9.6 D21–D22 shapes — runs between voluntary blocks, share past the boot slice, program-level gaps"
```

---

### Task 3: `shapes.py` — `tracker`'s job end

**Files:**
- Modify: `dataset/tools/meas/build/shapes.py`
- Test: `dataset/tools/tests/test_meas_build.py`

**Interfaces:**
- Produces: `tracker_job_end(lines, start_mono_ns, start_real_ns) -> float | None` (CLOCK_MONOTONIC s).

- [ ] **Step 1: Write the failing tests**

Append:

```python
MINER_LOG = [
    "Tracker-Message: 10:39:05.135: (Miner:'TrackerMinerFiles') set property:'status' to 'Idle'\n",
    "Tracker-Message: 10:39:05.281: (Miner:'TrackerMinerFiles') set property:'status' to 'Crawling recursively directory 'file:///x''\n",
    "Tracker-Message: 10:39:07.948: (Miner:'TrackerMinerFiles') set property:'status' to 'Idle'\n",
    "Tracker-Message: 10:39:08.033: (Miner:'TrackerMinerFiles') set property:'status' to 'Extracting metadata'\n",
    "Tracker-Message: 10:39:10.069: (Miner:'TrackerExtractDecorator') set property:'status' to 'Idle'\n",
    "Tracker-Message: 10:39:10.070: (Miner:'TrackerMinerFiles') set property:'status' to 'Idle'\n",
    "Tracker-Message: 10:39:20.177: (Miner:'TrackerMinerFiles') set property:'status' to 'Idle'\n",
]


def test_tracker_job_end_is_the_idle_after_the_last_busy_status():
    # repeat 4's tracker phase start edge: 2026-09-18 10:39:01.876931750 UTC
    t = shapes.tracker_job_end(MINER_LOG, 5383795831633, 1789727941876931750)
    assert t == pytest.approx(5383.795831633 + 8.19306825, abs=1e-5)


def test_tracker_job_end_none_without_a_job():
    assert shapes.tracker_job_end(MINER_LOG[:1], 5383795831633, 1789727941876931750) is None
```

- [ ] **Step 2: Run the tests to see them fail**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q -k tracker`
Expected: FAIL — `AttributeError: module 'meas.build.shapes' has no attribute 'tracker_job_end'`.

- [ ] **Step 3: Implement**

Append to `dataset/tools/meas/build/shapes.py`:

```python
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
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add dataset/tools/meas/build/shapes.py dataset/tools/tests/test_meas_build.py
git commit -m "feat(jioh/phase-9): 9.6 D16 shapes — tracker's job end from the miner's own Idle status"
```

---

### Task 4: `shapes.py` — object-job member steps

**Files:**
- Modify: `dataset/tools/meas/build/shapes.py`
- Test: `dataset/tools/tests/test_meas_build.py`

**Interfaces:**
- Consumes: `analyze.jobs_of` output (dicts with `kind`, `roles` sorted, `members`); `role: pid -> comm`; `parent_pid: pid -> pid`.
- Produces: `member_steps(jobs, role, parent_pid, segs_by_pid, fork_time, exit_time) -> {"jobs": int, "steps": {"<role> <k>/<n>": [ms]}, "child_order": {"<role>: <child roles by fork>": int}}`.

- [ ] **Step 1: Write the failing test**

Append:

```python
def test_member_steps_split_each_member_at_its_childrens_exits():
    role = {10: "sh", 11: "gcc", 12: "cc1", 13: "as", 14: "fixdep", 15: "rm", 16: "mkdir",
            20: "sh", 21: "gcc", 22: "cc1", 23: "as", 24: "fixdep", 25: "rm"}
    parent = {11: 10, 12: 11, 13: 11, 14: 10, 15: 10, 16: 10, 21: 20, 22: 21, 23: 21, 24: 20, 25: 20}
    fork = {11: 1.00, 12: 1.01, 13: 1.50, 14: 2.00, 15: 2.10, 16: 0.995, 21: 5.0, 22: 5.01, 23: 5.5, 24: 6.0, 25: 6.1}
    exit_ = {12: 1.40, 13: 1.60, 11: 1.70, 14: 2.05, 15: 2.20, 10: 2.30, 16: 0.999}
    def s(t, run, pid):
        return build.Seg(t, t, t + run / 1000, run, role[pid], pid, pid, "S", 3)
    segs = {10: [s(0.99, 0.7, 10), s(1.71, 0.1, 10), s(2.06, 0.1, 10), s(2.21, 0.13, 10)],
            11: [s(1.00, 1.7, 11), s(1.41, 0.15, 11), s(1.61, 0.34, 11)],
            12: [s(1.02, 300.0, 12)], 13: [s(1.51, 3.0, 13)], 14: [s(2.01, 5.6, 14)], 15: [s(2.11, 1.0, 15)]}
    six = ["as", "cc1", "fixdep", "gcc", "rm", "sh"]
    jobs = [{"kind": "object", "roles": six, "members": [10, 11, 12, 13, 14, 15]},
            {"kind": "object", "roles": sorted(six + ["mkdir"]), "members": [20, 21, 22, 23, 24, 25, 16]},
            {"kind": "helper", "roles": ["sh"], "members": [30]}]
    got = shapes.member_steps(jobs, role, parent, segs, fork, exit_)
    assert got["jobs"] == 1
    assert got["steps"]["sh 1/4"] == pytest.approx([0.7]) and got["steps"]["sh 2/4"] == pytest.approx([0.1])
    assert got["steps"]["sh 3/4"] == pytest.approx([0.1]) and got["steps"]["sh 4/4"] == pytest.approx([0.13])
    assert got["steps"]["gcc 1/3"] == pytest.approx([1.7]) and got["steps"]["gcc 2/3"] == pytest.approx([0.15])
    assert got["steps"]["gcc 3/3"] == pytest.approx([0.34]) and got["steps"]["cc1 1/1"] == pytest.approx([300.0])
    assert got["child_order"] == {"sh: gcc fixdep rm": 1, "gcc: cc1 as": 1}
```

- [ ] **Step 2: Run the test to see it fail**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q -k member_steps`
Expected: FAIL — `AttributeError: module 'meas.build.shapes' has no attribute 'member_steps'`.

- [ ] **Step 3: Implement**

Append to `dataset/tools/meas/build/shapes.py`:

```python
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
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add dataset/tools/meas/build/shapes.py dataset/tools/tests/test_meas_build.py
git commit -m "feat(jioh/phase-9): 9.6 D20 shapes — object-job member CPU per structural step, child order"
```

---

### Task 5: `analyze.py` wiring

**Files:**
- Modify: `dataset/tools/meas/build/analyze.py` (imports after line 36; `BATCH_PROGRAM` line 60–61; `batch()` 427–466; `analyze_phase()` 469–520; `load_edges()` 523–543; `main()` 546–593)
- Test: `dataset/tools/tests/test_meas_build.py`

**Interfaces:**
- Consumes: `shapes.*` (Tasks 2–4).
- Produces: per make phase `res["object_members"] = {"jobs", "child_order", "step_cpu_ms": {key: dist}, "_samples": {"steps": {key: [ms]}}}`; per batch phase `res["batch"]` gains `job_s, saturation_job, share_past_boot_slice, runs_between_blocks_n, gaps_n, _samples: {"runs_between_blocks_ms", "gaps_ms"}`; `load_edges()` gains `<edge>_real` (ns).

- [ ] **Step 1: Write the failing test**

Append:

```python
def test_batch_reads_the_job_window_and_shape():
    tree = {7, 8}
    tid2pid = {7: 7, 8: 7}
    role = {7: "clamscan"}
    segs = [build.Seg(1.000, 1.000, 1.012, 12.0, "clamscan", 7, 7, "D", 3),
            build.Seg(1.0122, 1.0122, 1.0202, 8.0, "clamscan", 7, 7, "D", 3),
            build.Seg(1.0205, 1.0205, 1.0215, 1.0, "clamscan", 7, 7, "Z", 3)]
    recs = {7: {"cpu_ns": 21_000_000, "etime_us": 21500, "blkio_ns": 0, "blkio_invalid_threads": 0}}
    b = build.batch("clamscan", tree, tid2pid, role, segs, {7: [1.0, 1.0122, 1.0205]}, 3, recs, 0.03)
    assert b["share_past_boot_slice"] == pytest.approx(2.0 / 21.0, abs=1e-4)
    assert b["_samples"]["runs_between_blocks_ms"] == pytest.approx([12.0, 8.0, 1.0])
    assert b["_samples"]["gaps_ms"] == pytest.approx([0.2, 0.3])
    assert b["job_s"] == pytest.approx(0.0215, abs=1e-6)
    cut = build.batch("clamscan", tree, tid2pid, role, segs, {}, 3, recs, 0.03, job_end=1.0203)
    assert cut["job_s"] == pytest.approx(0.0203, abs=1e-6) and cut["_samples"]["runs_between_blocks_ms"] == pytest.approx([12.0, 8.0])
```

- [ ] **Step 2: Run the test to see it fail**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q -k job_window`
Expected: FAIL — `KeyError: 'share_past_boot_slice'`.

- [ ] **Step 3: Implement**

(a) After the line `pct, TASK = _campaign_analyze.pct, _campaign_analyze.TASK …` add:

```python
try:
    from . import shapes          # imported as meas.build.analyze
except ImportError:
    import shapes                 # run as a script, or imported by pool.py with this directory on sys.path
```

(b) `BATCH_PROGRAM`'s `tracker` entry becomes `("tracker-miner-f", "tracker-extract", "gst-plugin-scan")` with the comment `# the miner, the extractor and the miner's gst-plugin-scan child are one indexing job (method §8, 2026-09-19 first entry)`.

(c) `batch()`: the signature becomes `def batch(phase, tree, tid2pid, role, segs, wakeups, meas_cpu, recs, cmd_wall_s, job_end=None):`, the docstring gains `job_end (s): the end of the program's job when it outlives it (D16; tracker); runs, gaps and the saturation over the job are read from the job's segments (D21, D22).`, and before `other = sorted(...)` insert:

```python
    start = min((s.t_in for s in rows), default=None)
    end = job_end if job_end is not None else max((s.t_end for s in rows), default=None)
    job_rows = [s for s in rows if s.t_in < end] if end is not None else []
    runs = shapes.runs_between_blocks(job_rows)
    gaps = shapes.program_gaps(job_rows, start, end) if job_rows else []
    job_s = (end - start) if job_rows else None
    share = shapes.share_past_slice(runs)
```

and add to the returned dict:

```python
            "job_s": round(job_s, 6) if job_s else None,
            "saturation_job": round(sum(s.run for s in job_rows) / 1000.0 / job_s, 4) if job_s else None,
            "share_past_boot_slice": round(share, 4) if share is not None else None,
            "runs_between_blocks_n": len(runs), "gaps_n": len(gaps),
            "_samples": {"runs_between_blocks_ms": runs, "gaps_ms": gaps},
```

(d) `load_edges()`: after `edges[e["phase"]][e["edge"]] = e["mono_ns"]` add `edges[e["phase"]][e["edge"] + "_real"] = e.get("real_ns")`.

(e) `analyze_phase()`: in the make/dkms block, after `res["dispatch"] = dispatch(...)`, insert:

```python
        exit_t = {pid: t for pid, (t, _c) in exits.items()}
        for pid, rec in recs.items():
            exit_t.setdefault(pid, rec["t_exit"])
        segs_by_pid = defaultdict(list)
        for s in segs:
            if s.cpu == meas_cpu and s.tid in tree:
                segs_by_pid[tid2pid.get(s.tid, s.tid)].append(s)
        om = shapes.member_steps(jobs, role, parent_pid, segs_by_pid, fork_t, exit_t)
        res["object_members"] = {"jobs": om["jobs"], "child_order": om["child_order"],
                                 "step_cpu_ms": {k: dist(v) for k, v in sorted(om["steps"].items())},
                                 "_samples": {"steps": om["steps"]}}
```

and replace the `else:` branch's `res["batch"] = batch(...)` with:

```python
        job_end = None
        log = os.path.join(D, "tracker.miner.log")
        if phase == "tracker" and os.path.exists(log) and e.get("start") and e.get("start_real"):
            with open(log, errors="replace") as handle:
                job_end = shapes.tracker_job_end(handle, e["start"], e["start_real"])
        res["batch"] = batch(phase, tree, tid2pid, role, segs, wakeups, meas_cpu, recs, cmd_wall_s, job_end)
```

(f) `main()`: the `_samples` strip becomes

```python
            for r in out["phases"].values():
                r.pop("_samples", None)
                for k in ("dispatch", "batch", "object_members"):
                    if k in r:
                        r[k].pop("_samples", None)
```

the batch print becomes `print(f"  batch {({k: v for k, v in r['batch'].items() if k != '_samples'})}")`, and after the jobs print add

```python
        if "object_members" in r:
            om = r["object_members"]
            print(f"  object jobs with the six members {om['jobs']}; step CPU p50 ms "
                  + ", ".join(f"{k} {v.get('p50')}" for k, v in om["step_cpu_ms"].items()))
            print(f"  child orders {om['child_order']}")
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py dataset/tools/tests/test_meas.py -q`
Expected: all pass.

- [ ] **Step 5: Check on repeat 4's records**

Run: `python3.12 dataset/tools/meas/build/analyze.py ~/.cache/meas-loop/pool/build-build-from10/meas-build-r4-full --phase tracker --phase clamscan --phase build-j8-warm`
Expected, against this session's readings of repeat 4: `tracker` `job_s` ≈ 5.108 and `saturation_job` ≈ 0.954; `clamscan` `share_past_boot_slice` ≈ 0.109; object jobs with the six members 2857, `sh 1/4` p50 ≈ 0.726 ms, `gcc 1/3` ≈ 1.707 ms; child orders `sh: gcc fixdep rm` 2857 and `gcc: cc1 as` 2857. A difference beyond the last digit is investigated before the commit (runs now close at a thread's exit and gaps count runnable time, so small differences from the session's quick readings are expected and are named in the commit message).

- [ ] **Step 6: Commit**

```bash
git add dataset/tools/meas/build/analyze.py dataset/tools/tests/test_meas_build.py
git commit -m "feat(jioh/phase-9): 9.6 analyzer — object-job member steps, cpu-batch runs, gaps and share past the slice, tracker over its job window"
```

---

### Task 6: `pool.py` — pooled tables, the D23/D24 criterion, results sections

**Files:**
- Modify: `dataset/tools/meas/build/pool.py`
- Test: `dataset/tools/tests/test_meas_build.py`

**Interfaces:**
- Consumes: Task 5's per-repeat fields; `stability(…, abs_floor, min_k)`.
- Produces: `out["phases"][make phase]["object_members"] = {"jobs": {r}, "child_order": {r}, "step_cpu_us": {key: pooled}}`; `out["phases"][batch phase]["shape"] = {"runs_between_blocks_us": pooled, "gaps_us": pooled, "share_past_boot_slice": {r: float}, "share_pooled": float}`; `criterion(out) -> {name: stability dict}`; `ABS_FLOOR_US = 1.0`, `MIN_REPEATS = 5`; `--title`.

- [ ] **Step 1: Write the failing test**

Append:

```python
from meas.build import pool


def test_criterion_lists_every_carried_value():
    rp = lambda *v: {"repeat_p50": dict(zip((4, 5, 7, 8, 9), v))}
    out = {"phases": {
        "build-j8-warm": {"roles": {n: {"cpu_per_process_us": rp(100, 101, 100, 102, 101)} for n in pool.CRITERION_ROLES},
                          "dispatch": {"per_dispatch_us": rp(670, 675, 673, 681, 676)},
                          "object_members": {"step_cpu_us": {"sh 1/4": rp(726, 785, 752, 785, 760)}}},
        "ffmpeg": {"shape": {"runs_between_blocks_us": rp(7, 7, 6, 6, 7), "gaps_us": rp(1, 1, 1, 1, 1),
                             "share_past_boot_slice": dict(zip((4, 5, 7, 8, 9), (0.702, 0.698, 0.696, 0.704, 0.700)))}}}}
    crit = pool.criterion(out)
    assert set(crit) == {f"{n} CPU per process" for n in pool.CRITERION_ROLES} | {
        "make dispatch", "object-job sh 1/4", "ffmpeg run between blocks", "ffmpeg program-level gap",
        "ffmpeg share past the boot slice"}
    assert crit["ffmpeg run between blocks"]["passes"] is True        # within the 1 µs floor
    assert all(c["k"] == 5 for c in crit.values())
    four = {"phases": {"ffmpeg": {"shape": {"runs_between_blocks_us": rp(7, 7, 7, 7), "gaps_us": rp(1, 1, 1, 1),
                                            "share_past_boot_slice": {4: 0.7, 5: 0.7, 7: 0.7, 8: 0.7}}}}}
    assert not any(c["passes"] for c in pool.criterion(four).values())    # four repeats: below the minimum
```

- [ ] **Step 2: Run the test to see it fail**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py -q -k criterion`
Expected: FAIL — `AttributeError: module 'meas.build.pool' has no attribute 'criterion'`.

- [ ] **Step 3: Implement**

(a) After `from stability import stability, TOLERANCE` add `import shapes  # noqa: E402` (the build directory is already on `sys.path`) and after `CRITERION_ROLES = …` add:

```python
ABS_FLOOR_US = 1.0   # the trace's resolution: perf sched timehist times in whole microseconds (D23)
MIN_REPEATS = 5      # kalibera-ismm13 §11 (D24)


def criterion(out):
    """The stability criterion's quantities and verdicts (method §8, the 2026-09-19 third and fourth entries; changelog
    D23, D24): D11's seven medians, the object-job members' step CPU, and per bound program its run-between-blocks
    and program-level gap medians and its share of CPU past the boot slice; tolerance the larger of 5 % of the mean
    and 1 µs, at least five repeats."""
    crit = {}
    w = out["phases"].get("build-j8-warm", {})
    for n in CRITERION_ROLES:
        if n in w.get("roles", {}):
            crit[n + " CPU per process"] = stability(w["roles"][n]["cpu_per_process_us"]["repeat_p50"], ABS_FLOOR_US, MIN_REPEATS)
    if "dispatch" in w:
        crit["make dispatch"] = stability(w["dispatch"]["per_dispatch_us"]["repeat_p50"], ABS_FLOOR_US, MIN_REPEATS)
    for k, t in w.get("object_members", {}).get("step_cpu_us", {}).items():
        crit[f"object-job {k}"] = stability(t["repeat_p50"], ABS_FLOOR_US, MIN_REPEATS)
    for ph in BATCH_PHASES:
        s = out["phases"].get(ph, {}).get("shape")
        if s:
            crit[f"{ph} run between blocks"] = stability(s["runs_between_blocks_us"]["repeat_p50"], ABS_FLOOR_US, MIN_REPEATS)
            crit[f"{ph} program-level gap"] = stability(s["gaps_us"]["repeat_p50"], ABS_FLOOR_US, MIN_REPEATS)
            crit[f"{ph} share past the boot slice"] = stability(s["share_past_boot_slice"], None, MIN_REPEATS)
    return crit
```

(b) `main()`: add `ap.add_argument("--title", help="the H1 of results.md (tag, runs, repeats, machine)")`. In the make-phase block, after `P["dispatch"] = {…}`, add:

```python
            om = {r: per[r]["phases"][ph]["object_members"] for r in have}
            keys = sorted({k for r in have for k in om[r]["_samples"]["steps"]})
            P["object_members"] = {"jobs": {r: om[r]["jobs"] for r in have},
                                   "child_order": {r: om[r]["child_order"] for r in have},
                                   "step_cpu_us": {k: pooled({r: om[r]["_samples"]["steps"].get(k, []) for r in have}, 1000.0) for k in keys}}
```

Replace `P["batch"] = {r: per[r]["phases"][ph]["batch"] for r in have}` with:

```python
            P["batch"] = {r: {k: v for k, v in per[r]["phases"][ph]["batch"].items() if k != "_samples"} for r in have}
            smp = {r: per[r]["phases"][ph]["batch"]["_samples"] for r in have}
            P["shape"] = {"runs_between_blocks_us": pooled({r: smp[r]["runs_between_blocks_ms"] for r in have}, 1000.0),
                          "gaps_us": pooled({r: smp[r]["gaps_ms"] for r in have}, 1000.0),
                          "share_past_boot_slice": {r: per[r]["phases"][ph]["batch"]["share_past_boot_slice"] for r in have},
                          "share_pooled": round(shapes.share_past_slice([x for r in have for x in smp[r]["runs_between_blocks_ms"]]) or 0.0, 4)}
```

Replace the criterion block (from `crit, cross = {}, {}` through the four lines that fill `crit`) with `crit, cross = criterion(out), {}` and `w = out["phases"].get("build-j8-warm", {})`, keeping the cross-machine loop. The `out["stability"]` line becomes `{"tolerance": TOLERANCE, "abs_floor_us": ABS_FLOOR_US, "min_repeats": MIN_REPEATS, "quantities": crit, "passes": bool(crit) and all(c["passes"] for c in crit.values())}`, and `render(out)` is called as `render(out, args.title)`.

(c) `render(out, title=None)`: the first line becomes `f"# {title or '9.6 build campaign — pooled results'}"`. After the job-shapes lines of a make phase add:

```python
        if "object_members" in P:
            om = P["object_members"]
            L += [f"object jobs with D19's six members {om['jobs']}; child order per repeat {om['child_order']}", "",
                  "| member step (D20) | n | CPU (µs) | spread (per-repeat p50) |", "|---|---|---|---|"]
            for k, t in om["step_cpu_us"].items():
                L.append(f"| `{k}` | {t['n']} | {fmt_q(t['q'])} | {t['repeat_p50']} |")
            L.append("")
```

In the batch table the header gains `job s | saturation over the job |` after `lifetime s |` (and one more `---|`), the row gains `{b.get('job_s')} | {b.get('saturation_job')} |` after `{b['lifetime_s']} |`, and after the table add:

```python
            s = P["shape"]
            L += [f"shape (D21, D22): runs between voluntary blocks (µs) {fmt_q(s['runs_between_blocks_us']['q'])} (n {s['runs_between_blocks_us']['n']}; spread {s['runs_between_blocks_us']['repeat_p50']}); "
                  f"program-level gaps (µs) {fmt_q(s['gaps_us']['q'])} (n {s['gaps_us']['n']}; spread {s['gaps_us']['repeat_p50']}); "
                  f"share of CPU past the boot slice {s['share_past_boot_slice']} (pooled {s['share_pooled']})", ""]
```

The stability section's heading becomes `## Same-machine repeats and the stability criterion (D10, D11, D23, D24)`, its criterion sentence `Criterion: the 95 % confidence half-width of the across-repeat mean of each carried value is at most the larger of {st['tolerance']:.0%} of the mean and {st['abs_floor_us']} µs, over at least {st['min_repeats']} repeats; repeats are added one at a time until it holds (D11, D23, D24).`, its table header `| quantity | repeats | mean | spread (cv) | 95 % half-width | half-width (abs) | leave-one-out | passes |` with one more `---|`, and each row

```python
            cv = "–" if c["cv"] is None else f"{c['cv']:.1%}"
            hw = "–" if c["half_width"] is None else f"±{c['half_width']:.1%}"
            loo = "–" if c["leave_one_out"] is None else f"{c['leave_one_out']:.1%}"
            L.append(f"| {q} | {c['k']} | {c['mean']} | {cv} | {hw} | {c['half_width_abs']} | {loo} | {'yes' if c['passes'] else 'no'} |")
```

- [ ] **Step 4: Run the tests to see them pass**

Run: `python3.12 -m pytest dataset/tools/tests/test_meas_build.py dataset/tools/tests/test_meas.py -q`
Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add dataset/tools/meas/build/pool.py dataset/tools/tests/test_meas_build.py
git commit -m "feat(jioh/phase-9): 9.6 pool — member step and cpu-batch shape tables, the D23–D24 criterion over every carried value, results sections"
```

---

### Task 7: the four-repeat pool regenerated and checked

**Files:**
- Modify: `_dev/research/jioh/task-9.6-compile/campaign/results.md`, `_dev/research/jioh/task-9.6-compile/campaign/results/pooled.json`
- Modify (only if the status differs): `_dev/research/jioh/task-9.6-compile/campaign/method.md` §8

- [ ] **Step 1: Put the gated jobs' reports beside the measured repeats**

The committed pool lists the four gated jobs (repeats 1, 2, 3, 6 of run 35328071379); `pool_runs.py` downloads only landed jobs. Run:

```bash
P=~/.cache/meas-loop/pool/build-build-from10
for k in 1 2 3 6; do gh run download 35328071379 -n meas-build-r$k-full -D $P/meas-build-r$k-full; done
ls $P
```

Expected: eight `meas-build-r*-full` folders.

- [ ] **Step 2: Pool into the scratchpad**

```bash
S=/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/f2295b7c-9ebd-4e56-8583-c5ea37e8258a/scratchpad/pool4
mkdir -p $S
python3.12 dataset/tools/meas/build/pool.py ~/.cache/meas-loop/pool/build-build-from10 $S/pooled.json --md $S/results.md --cpu-model "EPYC 7763" \
  --title "9.6 build campaign — pooled results (meas-ci:build:2026-09-18; runs 35328071379, 35328873409, 35337322204; repeats 4, 5, 7, 8 on the AMD EPYC 7763, full mode; D11)"
diff _dev/research/jioh/task-9.6-compile/campaign/results.md $S/results.md | head -80
```

Expected: `pooled 4 repeat(s)`; the diff shows only the new sections, the batch table's two new columns, the `tracker` rows that now include `gst-plugin-scan` (a few ms), and the extended stability table, whose verdict is "Does not hold yet" (four repeats, below the minimum). Any other change is investigated before going on.

- [ ] **Step 3: Check the numbers against the session's readings**

In `$S/results.md`: share past the boot slice per repeat — `clamscan` 0.107–0.115, `ffmpeg` 0.696–0.704, `HandBrakeCLI` 0.624–0.627, `python3` 0.917–0.920, `tracker` 0.530–0.536; `tracker` saturation over the job 0.954–0.962; `sh 1/4` spread 0.726–0.785 ms (±6.0 %); `gcc` steps ±2.6–3.1 %. Small differences follow from the definitions fixed in Tasks 2 and 5 (a thread's last run counted; runnable time counted as busy in the gaps). Note every value whose half-width lands on the other side of the tolerance from the method's "At repeats 4, 5, 7, 8" status line.

- [ ] **Step 4: Put the pool in place**

```bash
cp $S/results.md _dev/research/jioh/task-9.6-compile/campaign/results.md
cp $S/pooled.json _dev/research/jioh/task-9.6-compile/campaign/results/pooled.json
```

If Step 3 found a value on the other side of the tolerance, append to `campaign/method.md` §8 one dated line: `- 2026-09-19, the status at four repeats as the tooling reads it (results.md): <quantities and half-widths that differ from the third 2026-09-19 entry>; the list, tolerance and procedure stand.`

- [ ] **Step 5: Commit** (the message's parenthesis also names each quantity whose half-width is over the tolerance, from Step 3)

```bash
git add _dev/research/jioh/task-9.6-compile/campaign/results.md _dev/research/jioh/task-9.6-compile/campaign/results/pooled.json _dev/research/jioh/task-9.6-compile/campaign/method.md
git commit -m "chore(jioh/phase-9): 9.6 four-repeat pool regenerated with the carried quantities — criterion does not hold yet (below five repeats)"
```
