"""The untraced control's collection tooling (`_dev/docs/spec/jioh/task-9.5-untraced-control.md`)."""

import importlib.util
import pathlib
import re

MEAS = pathlib.Path(__file__).resolve().parents[1] / "meas"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


snapshot = _load("snapshot_for_control", MEAS / "probe" / "snapshot.py")


def _stat(pid, comm, ppid, start):
    # fields 3 on: state, ppid, eight zeros, utime, stime, six zeros, starttime (field 22)
    rest = ["S", str(ppid)] + ["0"] * 9 + ["7", "3"] + ["0"] * 6 + [str(start), "0"]
    return f"{pid} ({comm}) " + " ".join(rest) + "\n"


def _process(root, pid, comm, cmd, cgroup, tasks, ppid=1):
    """A fake /proc/<pid>: `tasks` maps tid -> (comm, start, run_ns, wait_ns, slices, vol, invol)."""
    d = root / str(pid)
    (d / "task").mkdir(parents=True)
    (d / "cmdline").write_text(cmd.replace(" ", "\0") + "\0")
    (d / "comm").write_text(comm + "\n")
    (d / "cgroup").write_text(f"0::{cgroup}\n")
    (d / "stat").write_text(_stat(pid, comm, ppid, tasks[pid][1]))
    for tid, (tcomm, start, run, wait, slices, vol, invol) in tasks.items():
        t = d / "task" / str(tid)
        t.mkdir()
        (t / "stat").write_text(_stat(tid, tcomm, ppid, start))
        if run is not None:
            (t / "schedstat").write_text(f"{run} {wait} {slices}\n")
        (t / "status").write_text(f"Name:\t{tcomm}\nvoluntary_ctxt_switches:\t{vol}\nnonvoluntary_ctxt_switches:\t{invol}\n")


def _fake_proc(root):
    _process(root, 100, "soffice.bin", "/usr/lib/libreoffice/program/soffice.bin --norestore /tmp/doc/large.odt",
             "/user.slice/user-1001.slice/session-3.scope",
             {100: ("soffice.bin", 5000, 123456789, 1000, 42, 30, 12), 101: ("gmain", 5001, 2000, 10, 3, 2, 1)})
    _process(root, 120, "oosplash", "/usr/lib/libreoffice/program/oosplash", "/user.slice",
             {120: ("oosplash", 4990, 900, 0, 1, 1, 0), 121: ("gone", 4991, None, None, None, 0, 0)}, ppid=100)
    _process(root, 200, "bash", "bash", "/user.slice", {200: ("bash", 10, 5, 0, 1, 1, 0)})


def test_the_snapshot_reads_each_threads_runtime_and_switches(tmp_path, monkeypatch):
    # decision 9: each thread's CPU from task/<tid>/schedstat (ns), its switches from task/<tid>/status, and its
    # start time, which tells a reused tid from the thread it replaced
    _fake_proc(tmp_path)
    monkeypatch.setattr(snapshot, "PROC", str(tmp_path))
    snap = snapshot.snapshot("soffice", None)
    procs = {p["pid"]: p for p in snap["procs"]}
    assert sorted(procs) == [100, 120]                         # the matching root and its descendant, not bash
    assert procs[100]["cgroup"] == "/user.slice/user-1001.slice/session-3.scope"
    tasks = {t["tid"]: t for t in procs[100]["tasks"]}
    assert tasks[100] == {"tid": 100, "comm": "soffice.bin", "start_ticks": 5000, "run_ns": 123456789,
                          "wait_ns": 1000, "slices": 42, "vol": 30, "invol": 12}
    assert tasks[101]["comm"] == "gmain" and tasks[101]["run_ns"] == 2000


def test_a_thread_that_left_mid_read_is_skipped(tmp_path, monkeypatch):
    _fake_proc(tmp_path)
    monkeypatch.setattr(snapshot, "PROC", str(tmp_path))
    procs = {p["pid"]: p for p in snapshot.snapshot("soffice", None)["procs"]}
    assert [t["tid"] for t in procs[120]["tasks"]] == [120]    # 121's schedstat is gone


def test_the_tree_totals_are_kept(tmp_path, monkeypatch):
    _fake_proc(tmp_path)
    monkeypatch.setattr(snapshot, "PROC", str(tmp_path))
    snap = snapshot.snapshot("soffice", None)
    assert snap["n_procs"] == 2 and snap["n_threads"] == 4
    assert snap["vol_switches"] == 30 + 2 + 1 + 0 and snap["nonvol_switches"] == 12 + 1
