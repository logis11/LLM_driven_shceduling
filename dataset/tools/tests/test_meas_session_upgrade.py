"""The reading of 9.10's upgrade probe (session/upgrade_probe.py; 9.10 D165–D167) on a constructed run."""
import gzip
import json

from meas.session import upgrade_probe

UM = "/user.slice/user-1001.slice/user@1001.service"


def _run(tmp_path):
    D = tmp_path
    procs = [{"pid": 1, "ppid": 0, "comm": "systemd", "cmd": "/sbin/init", "cgroup": "/init.scope", "kthread": False},
             {"pid": 2, "ppid": 0, "comm": "kthreadd", "cmd": "", "cgroup": "/", "kthread": True},
             {"pid": 10, "ppid": 1, "comm": "gnome-shell", "cmd": "/usr/bin/gnome-shell",
              "cgroup": UM + "/session.slice/org.gnome.Shell@wayland.service", "kthread": False},
             {"pid": 20, "ppid": 1, "comm": "dbus-daemon", "cmd": "dbus-daemon --system",
              "cgroup": "/system.slice/dbus.service", "kthread": False},
             {"pid": 50, "ppid": 40, "comm": "bash", "cmd": "bash run.sh", "cgroup": "/system.slice/runner.service",
              "kthread": False},
             {"pid": 60, "ppid": 50, "comm": "sudo", "cmd": "sudo perf", "cgroup": "/system.slice/runner.service",
              "kthread": False}]
    inst = {"systemd": {"pid1": [1]}, "gnome-shell": {"gnome-shell": [10]}, "dbus-daemon": {"system-bus": [20]}}
    json.dump({"procs": procs, "instances": inst, "kthreads": [2]}, open(D / "census.probe.start.json", "w"))
    notifier = {"pid": 600, "ppid": 10, "comm": "update-notifier", "cmd": "update-notifier",
                "cgroup": UM + "/app.slice/update-notifier.service", "kthread": False}
    json.dump({"procs": procs + [notifier], "instances": inst, "kthreads": [2]}, open(D / "census.probe.end.json", "w"))
    (D / "report.kv").write_text("harness.pid=50\nupgrade.unit.result=success\n")
    with open(D / "edges.mono.jsonl", "w") as f:
        for w, a, b in (("pre", 100, 110), ("job", 110, 120), ("post", 120, 140)):
            f.write(json.dumps({"phase": w, "edge": "start", "mono_ns": a * 10**9}) + "\n")
            f.write(json.dumps({"phase": w, "edge": "end", "mono_ns": b * 10**9}) + "\n")
    # timehist: time [cpu] comm[tid/pid] wait delay run(ms) state
    rows = [(105.0, "systemd[1]", 1.0), (115.0, "systemd[1]", 5.0), (105.0, "gnome-shell[10]", 0.2),
            (125.0, "gnome-shell[11/10]", 0.2), (111.0, "apt-helper[500]", 3.0), (112.5, "apt.systemd.dai[501]", 2.0),
            (113.0, "localedef[502]", 50.0), (119.8, "update-notifier[600]", 2.0), (109.0, "python3[700]", 1.0),
            (115.5, "kworker/3:1[800]", 0.1)]
    with gzip.open(D / "perf.upgrade-probe.timehist.txt.gz", "wt") as f:
        for t, task, run in rows:
            f.write(f"  {t:.6f} [0003]  {task}  0.000  0.010  {run:.3f}  S\n")
    forks = [(110.5, "systemd", 1, "systemd", 500), (110.6, None, 500, "/usr/lib/apt/apt-helper", None),
             (112.0, "systemd", 1, "systemd", 501), (112.1, None, 501, "/usr/lib/apt/apt.systemd.daily", None),
             (112.9, "apt.systemd.dai", 501, "apt.systemd.dai", 502), (119.5, "gnome-shell", 10, "gnome-shell", 600),
             (124.0, "gnome-shell", 10, "gnome-shell", 11), (108.9, "sudo", 60, "sudo", 700),
             (115.4, "kthreadd", 2, "kthreadd", 800)]
    with gzip.open(D / "perf.upgrade-probe.forks.txt.gz", "wt") as f:
        for t, comm, pid, child, cpid in forks:
            if comm is None:
                f.write(f"  {t:.6f}: sched:sched_process_exec: filename={child} pid={pid} old_pid={pid}\n")
            else:
                f.write(f"  {t:.6f}: sched:sched_process_fork: comm={comm} pid={pid} child_comm={child} child_pid={cpid}\n")
    return D


def test_the_job_is_pid_1_s_children_that_run_the_unit_s_commands_and_their_descendants(tmp_path):
    r = upgrade_probe.read(str(_run(tmp_path)))
    assert sorted(x["pid"] for x in r["job"]["roots"]) == [500, 501]
    assert r["job"]["processes"] == 3 and r["job"]["comms"] == ["apt-helper", "apt.systemd.dai", "localedef"]


def test_a_new_process_is_one_outside_the_census_the_job_the_harness_and_the_kernel(tmp_path):
    # the harness's python3 (a child of its sudo), the kernel worker and gnome-shell's new thread are not new processes
    r = upgrade_probe.read(str(_run(tmp_path)))
    assert [n["pid"] for n in r["new_processes"]] == [600]
    n = r["new_processes"][0]
    assert n["window"] == "job" and n["ancestor"]["comm"] == "gnome-shell" and n["cpu_ms"] == 2.0
    assert [x["pid"] for x in r["new_in_later_census"]] == [600]


def test_the_entries_work_is_read_per_window_as_cpu_and_runs(tmp_path):
    e = upgrade_probe.read(str(_run(tmp_path)))["entries"]
    assert e["systemd"]["pid1"]["pre"]["cpu_ms_per_s"] == 0.1 and e["systemd"]["pid1"]["job"]["cpu_ms_per_s"] == 0.5
    assert e["gnome-shell"]["gnome-shell"]["post"]["runs"] == 1        # the new thread's run is the shell's
    assert e["dbus-daemon"]["system-bus"]["job"]["runs"] == 0
