"""The DKMS build's readings for `module-build-orchestrator` and `module-compiler-child` (9.10 changelog D52–D55;
campaign/dkms/method.md §5).

Within the hook run that built the module, the make jobs (9.6's `jobs_of`, a job's members stopping at a nested
make) are split into the job kinds of D53, each carried as one canonical process tree:

  object   sh → gcc → cc1, as; sh → fixdep; sh → rm                        (9.6 D19's chain)
  kprobe   sh → mkdir; sh → gcc → cc1, as; sh → rm                         (kbuild's compiler probes)
  conftest sh → sh (conftest.sh) → dirname, gcc → cc1, rm, sh, sh          (NVIDIA's conftest tests; variant `a`)
           the same with gcc → cc1, as and a second rm                      (variant `b`, a test that assembles)

`gcc` is the compiler driver whatever its comm (`x86_64-linux-gn` here). A job is fitted to its kind's tree by
role, children in fork order; the fold rule (D53) carries what the tree does not name: a further process of a role
the tree has there (a second compile) adds its CPU to that member, step by step; a process of a role the tree has
not there (objtool, tr) adds its subtree's CPU to its parent member's step in which it was forked. Each member's CPU
per structural step is its segments on the measured CPU split at the exits of its own children (9.6 D20).

Also per hook run: the kinds in start order (D53's spawn order), make's dispatch run (9.6's reading), the serial
tail after the last object or link job as a batch loop (D54: runs between voluntary blocks and the block after
each), and the CPU split between what the entry carries and what it states unmodelled.
"""

import bisect
import os
import sys
from collections import defaultdict

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.build import analyze as _build   # noqa: E402
from meas.build import shapes  # noqa: E402

GCC = "gcc"
# (member id, role, children); a role "gcc" matches any compiler driver comm (is_gcc)
TREES = {
    "object": ("sh", "sh", [("gcc", GCC, [("cc1", "cc1", []), ("as", "as", [])]), ("fixdep", "fixdep", []), ("rm", "rm", [])]),
    "kprobe": ("sh", "sh", [("mkdir", "mkdir", []), ("gcc", GCC, [("cc1", "cc1", []), ("as", "as", [])]), ("rm", "rm", [])]),
    "conftest-a": ("sh", "sh", [("csh", "sh", [("dirname", "dirname", []), ("gcc", GCC, [("cc1", "cc1", [])]),
                                               ("rm", "rm", []), ("tsh1", "sh", []), ("tsh2", "sh", [])])]),
    "conftest-b": ("sh", "sh", [("csh", "sh", [("dirname", "dirname", []), ("gcc", GCC, [("cc1", "cc1", []), ("as", "as", [])]),
                                               ("rm", "rm", []), ("rm2", "rm", []), ("tsh1", "sh", []), ("tsh2", "sh", [])])]),
}
LETTER = {"object": "o", "kprobe": "p", "conftest-a": "c", "conftest-b": "C"}


def is_gcc(comm):
    return comm in ("gcc", "cc") or comm.startswith(("gcc-", "x86_64-linux-gn"))


def role_of(comm):
    return GCC if is_gcc(comm) else comm


def members(tree):
    """[(member id, role, n_steps)] in depth-first order."""
    out = []

    def walk(node):
        mid, role, kids = node
        out.append((mid, role, len(kids) + 1 if kids else 1))
        for k in kids:
            walk(k)
    walk(tree)
    return out


def kind_of(job, role, kids):
    """object | kprobe | conftest-a | conftest-b | None (helper, link, archive: not carried, D54)."""
    if job["kind"] == "object":
        return "object"
    if job["kind"] != "probe":
        return None
    if any(role.get(c) == "sh" for c in kids.get(job["root"], ())):
        return "conftest-b" if any(role.get(x) == "as" for x in job["members"]) else "conftest-a"
    return "kprobe"


def fit(job, tree, role, kids, fork_t, exit_t, cpu_segs):
    """{member id: [CPU ms per step]} for one job under the fold rule; (steps, exact) where exact is True when the
    job's processes are exactly the tree's."""
    steps = {mid: [0.0] * n for mid, _r, n in members(tree)}
    exact = [True]
    members_set = set(job["members"])

    def subtree_cpu(x):
        tot, stack = 0.0, [x]
        while stack:
            y = stack.pop()
            tot += sum(s.run for s in cpu_segs.get(y, ()))
            stack.extend(c for c in kids.get(y, ()) if c in members_set)
        return tot

    def place(x, node):
        mid, _role, cnodes = node
        ch = sorted((c for c in kids.get(x, ()) if c in members_set), key=lambda c: fork_t.get(c, 0.0))
        used, mapped, foreign = set(), [], []
        for c in ch:
            r = role_of(role.get(c, "?"))
            free = [i for i, cn in enumerate(cnodes) if cn[1] == r and i not in used]
            same = [i for i, cn in enumerate(cnodes) if cn[1] == r]
            if free:
                used.add(free[0]); mapped.append((c, cnodes[free[0]]))
            elif same:
                exact[0] = False; mapped.append((c, cnodes[same[-1]]))
            else:
                exact[0] = False; foreign.append(c)
        if len(used) < len(cnodes):
            exact[0] = False
        n = len(steps[mid])
        bounds = sorted(exit_t[c] for c, _cn in mapped if c in exit_t)
        for s in cpu_segs.get(x, ()):
            steps[mid][min(bisect.bisect_right(bounds, s.t_in), n - 1)] += s.run
        for c in foreign:
            steps[mid][min(bisect.bisect_right(bounds, fork_t.get(c, 0.0)), n - 1)] += subtree_cpu(c)
        for c, cn in mapped:
            place(c, cn)
    place(job["root"], tree)
    return steps, exact[0]


def jobs_of(tree, tid2pid, role, parent_pid, forks, exits, recs):
    """9.6's make jobs (`meas.build.analyze.jobs_of`, D2) with a job's members stopping at a nested make, whose
    children are jobs of their own: NVIDIA's top-level make runs kbuild's through a shell recipe."""
    children = defaultdict(list)
    for pid, pp in parent_pid.items():
        children[pp].append(pid)
    fork_t = {c: t for t, _p, _pc, c, _cc in forks}

    def exit_t(pid):
        if pid in exits:
            return exits[pid][0]
        r = recs.get(pid)
        return None if r is None else r["t_exit"]
    makes = {pid for pid in set(tid2pid.get(t, t) for t in tree) if role.get(pid) == "make"}
    jobs = []
    for m in makes:
        for c in children.get(m, ()):
            if role.get(c) == "make":
                continue
            mem, stack = [], [c]
            while stack:
                x = stack.pop(); mem.append(x)
                stack.extend(y for y in children.get(x, ()) if role.get(y) != "make")
            starts = [fork_t[x] for x in mem if x in fork_t]
            ends = [e for e in (exit_t(x) for x in mem) if e is not None]
            rs = sorted(role.get(x, "?") for x in mem)
            jobs.append({"root": c, "make": m, "members": mem, "roles": rs, "kind": _build.job_kind(rs),
                         "start": min(starts) if starts else None, "end": max(ends) if ends else None})
    jobs.sort(key=lambda j: (j["start"] is None, j["start"]))
    return jobs


def hook_run(hook_tids, segs, forks, recs, last_comm):
    """(tid2pid, role by pid, parent pid by pid) over one hook run's threads."""
    tid2pid = {s.tid: s.pid for s in segs}
    parent = {c: p for _t, p, _pc, c, _cc in forks}
    role = {pid: r["comm"] for pid, r in recs.items()}
    for t in hook_tids:
        role.setdefault(tid2pid.get(t, t), last_comm.get(t, "?"))
    parent_pid = {}
    for t in hook_tids:
        pid = tid2pid.get(t, t)
        p = parent.get(t)
        if p is not None and pid == t:
            parent_pid[pid] = tid2pid.get(p, p)
    return tid2pid, role, parent_pid


def readings(jobs, hook_tids, tid2pid, role, parent_pid, segs, forks, exits, recs, meas_cpu):
    """The hook run's readings (one dict; '_samples' holds the arrays the pool pools)."""
    kids = defaultdict(list)
    for c, p in parent_pid.items():
        kids[p].append(c)
    fork_t = {c: t for t, _p, _pc, c, _cc in forks}
    exit_t = {pid: t for pid, (t, _c) in exits.items()}
    for pid, r in recs.items():
        exit_t.setdefault(pid, r["t_exit"])
    on = [s for s in segs if s.cpu == meas_cpu and s.tid in hook_tids]
    cpu_segs = defaultdict(list)
    for s in on:
        cpu_segs[tid2pid.get(s.tid, s.tid)].append(s)
    cpu_pid = {p: sum(s.run for s in ss) for p, ss in cpu_segs.items()}

    counts, exact, seq = defaultdict(int), defaultdict(int), []
    steps = defaultdict(list)
    kind_cpu, carried_pids = defaultdict(float), set()
    for j in jobs:
        k = kind_of(j, role, kids)
        if k is None:
            continue
        st, ex = fit(j, TREES[k], role, kids, fork_t, exit_t, cpu_segs)
        counts[k] += 1; exact[k] += ex; seq.append(LETTER[k])
        for mid, vals in st.items():
            n = len(vals)
            for i, v in enumerate(vals):
                steps[f"{k} {mid} {i + 1}/{n}"].append(v)
        kind_cpu[k] += sum(cpu_pid.get(x, 0.0) for x in j["members"])
        carried_pids.update(j["members"])

    disp = _build.dispatch(hook_tids, tid2pid, role, segs, forks, meas_cpu, recs)
    make_pids = {tid2pid.get(t, t) for t in hook_tids if role.get(tid2pid.get(t, t)) == "make"}
    make_cpu = sum(cpu_pid.get(p, 0.0) for p in make_pids)

    ends = [j["end"] for j in jobs if j["kind"] in ("object", "link") and j["end"] is not None]
    t_last = max(ends) if ends else None
    in_job = {x for j in jobs for x in j["members"]}
    tail_rows = [s for s in on if t_last is not None and s.t_in >= t_last
                 and tid2pid.get(s.tid, s.tid) not in in_job and tid2pid.get(s.tid, s.tid) not in make_pids]
    tail_rows.sort(key=lambda s: s.t_in)
    tail_run = shapes.runs_between_blocks(tail_rows) if tail_rows else []
    tail_block = shapes.blocks_after_runs(tail_rows, tail_rows[0].t_in, max(s.t_end for s in tail_rows)) if tail_rows else []
    tail_cpu = sum(s.run for s in tail_rows)
    tail_by = defaultdict(float)
    for s in tail_rows:
        tail_by[role.get(tid2pid.get(s.tid, s.tid), "?")] += s.run

    total = sum(s.run for s in on)
    jobs_cpu = sum(kind_cpu.values())
    carried = jobs_cpu + make_cpu + tail_cpu
    return {"counts": dict(counts), "exact_fit": dict(exact), "sequence": "".join(seq),
            "cpu_ms": {"hook_run": round(total, 3), "jobs": {k: round(v, 3) for k, v in kind_cpu.items()},
                       "make": round(make_cpu, 3), "tail": round(tail_cpu, 3), "carried": round(carried, 3),
                       "unmodelled": round(total - carried, 3)},
            "carried_share": round(carried / total, 4) if total else None,
            "tail": {"start_s": t_last, "cpu_by_comm_ms": {k: round(v, 3) for k, v in sorted(tail_by.items(), key=lambda kv: -kv[1])},
                     "run_ms": _build.dist(tail_run), "block_ms": _build.dist(tail_block)},
            "dispatch": {k: v for k, v in disp.items() if k != "_samples"},
            "step_cpu_ms": {k: _build.dist(v) for k, v in sorted(steps.items())},
            "_samples": {"steps": dict(steps), "dispatch_ms": disp["_samples"]["per_dispatch_ms"],
                         "tail_run_ms": tail_run, "tail_block_ms": tail_block}}
