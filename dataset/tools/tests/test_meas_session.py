"""Constructed cases for the 9.9 session campaign tools (changelog D8–D14)."""

import json
import re

from meas.session import analyze, census, pool, size_steady

UID = 1002


def _proc(pid, comm, cgroup, ppid=1, kthread=False, cmd=None):
    return {"pid": pid, "ppid": ppid, "comm": comm, "cmd": cmd or comm, "uid": UID, "cgroup": cgroup,
            "cpus_allowed": "0-3", "threads": 1, "start_ticks": 0, "kthread": kthread}


U = f"/user.slice/user-{UID}.slice/user@{UID}.service"
PROCS = [
    _proc(1, "systemd", "/init.scope"),
    _proc(2, "kthreadd", "/", ppid=0, kthread=True),
    _proc(30, "kworker/3:1", "/", ppid=2, kthread=True),
    # D17: the system bus moves into the measured slice; the census matches it in either
    _proc(400, "dbus-daemon", "/meas.slice/dbus.service", cmd="@dbus-daemon --system --address=systemd:"),
    _proc(410, "snapd", "/system.slice/snapd.service"),
    _proc(500, "systemd", f"{U}/init.scope", cmd="/usr/lib/systemd/systemd --user"),
    # another user's manager, the runner's lingering one — not the measured user's
    _proc(501, "systemd", "/user.slice/user-1001.slice/user@1001.service/init.scope"),
    _proc(510, "dbus-daemon", f"{U}/session.slice/dbus.service", cmd="/usr/bin/dbus-daemon --session"),
    _proc(520, "gnome-shell", f"{U}/session.slice/org.gnome.Shell@wayland.service"),
    _proc(521, "Xwayland", f"{U}/session.slice/org.gnome.Shell@wayland.service"),
    _proc(530, "pipewire", f"{U}/session.slice/pipewire.service"),
    _proc(531, "wireplumber", f"{U}/session.slice/wireplumber.service"),
    _proc(532, "pipewire-pulse", f"{U}/session.slice/pipewire-pulse.service"),
    _proc(540, "gsd-power", f"{U}/session.slice/org.gnome.SettingsDaemon.Power.service"),
]


def test_the_census_names_each_instance_by_its_unit():
    # method §4, D4, D6, D7: pid 1 against the user manager, the two buses, the three PipeWire services
    inst, other = census.instances(PROCS, UID)
    assert inst["systemd"] == {"pid1": [1], "user-manager": [500]}
    assert inst["dbus-daemon"] == {"system-bus": [400], "session-bus": [510]}
    assert inst["pipewire"] == {"pipewire": [530], "wireplumber": [531], "pipewire-pulse": [532]}
    assert inst["gnome-shell"] == {"gnome-shell": [520]}
    # an Xwayland in the shell's unit is the unit's other process, reported, never the shell (the held question)
    assert [o["comm"] for o in other] == ["Xwayland"]


def test_the_system_bus_is_found_in_either_slice():
    for cg in ("/system.slice/dbus.service", "/meas.slice/dbus.service", "/system.slice/dbus-broker.service"):
        inst, _ = census.instances([_proc(400, "dbus-daemon", cg)], UID)
        assert inst["dbus-daemon"]["system-bus"] == [400], cg


def test_the_idle_state_needs_the_shield_the_blank_and_an_active_session():
    ok = {"session_active": True, "shield_active": True, "power_save_mode": 3}
    assert census.is_idle(ok)
    assert not census.is_idle({**ok, "power_save_mode": 0})      # the monitor on
    assert not census.is_idle({**ok, "power_save_mode": -1})     # unknown
    assert not census.is_idle({**ok, "shield_active": False})
    assert not census.is_idle({**ok, "session_active": None})    # the query failed


def test_the_placement_is_read_from_the_processes_not_the_units(tmp_path):
    # D21: `Slice=` applies when a unit starts, so the check reads each process's own allowed CPUs. The system bus
    # running since boot is the case that went unseen in the 2026-09-23 probes.
    procs = [dict(p) for p in PROCS]
    for p in procs:
        p["cpus_allowed"] = "0-2"
    by_pid = {p["pid"]: p for p in procs}
    for pid in (1, 500, 510, 520, 530, 531, 532):        # the entries, on the measured CPU
        by_pid[pid]["cpus_allowed"] = "3"
    by_pid[400]["cpus_allowed"] = "0-2"                  # the system bus, left in system.slice — the defect
    inst, _ = census.instances(procs, UID)
    c = {"procs": procs, "instances": inst}
    path = tmp_path / "census.json"
    path.write_text(json.dumps(c))
    bad = census.placed(str(path), "3")
    assert any("dbus-daemon/system-bus" in b and "cpus_allowed=0-2" in b for b in bad)
    assert not any("gnome-shell" in b for b in bad)

    by_pid[400]["cpus_allowed"] = "3"                    # restarted into meas.slice: the placement holds
    path.write_text(json.dumps(c))
    assert census.placed(str(path), "3") == []

    by_pid[410]["cpus_allowed"] = "3"                    # snapd, no entry of ours, allowed the measured CPU
    path.write_text(json.dumps(c))
    assert [b for b in census.placed(str(path), "3")] == [
        "not an entry: pid 410 snapd cpus_allowed=3 cgroup=/system.slice/snapd.service"]


def test_the_cpu_mask_is_the_bytes_start_transient_unit_takes():
    assert census.mask("0-2") == "ay 1 7"
    assert census.mask("3") == "ay 1 8"
    assert census.mask("0-2,9") == "ay 2 7 2"


def test_busctl_values_parse():
    assert census.busctl_value({"rc": 0, "out": "b true"}) is True
    assert census.busctl_value({"rc": 0, "out": "i 3"}) == 3
    assert census.busctl_value({"rc": 1, "out": ""}) is None


def _row(t, cpu, comm, tid, pid, run, state="S"):
    return f"{t:12.6f} [{cpu:04d}]  {comm}[{tid}/{pid}]    0.000      0.001      {run:.3f}      {state}\n"


def _run_dir(d, k=1, mode="full", foreign_user=False, scale=1.0, in_unit=False):
    inst, other = census.instances(PROCS, UID)
    c = {"instances": inst, "in_unit_other": other, "kthreads": [2, 30],
         "display_servers": [{"pid": 521, "comm": "Xwayland", "cmd": "Xwayland"}]}
    d.mkdir(parents=True, exist_ok=True)
    (d / "report.json").write_text(json.dumps({"app": "session", "repeat": k, "mode": mode, "gate": "open",
                                               "pin.load_cpu": "3", "edge.idle": "1", "version.gnome-shell": "46.0"}))
    (d / "spec.json").write_text(json.dumps({"cpu_model": "AMD EPYC 7763 64-Core Processor",
                                             "github_run": {"GITHUB_RUN_ID": f"9{k}"}}))
    for e in ("start", "end"):
        (d / f"census.steady.{e}.json").write_text(json.dumps(c))
    (d / "edges.jsonl").write_text(json.dumps({"phase": "steady", "edge": "start", "mono_ns": 0}) + "\n")
    rows = [_row(0.0, 0, "perf", 50, 50, 0.01, "R")]
    wakes = []
    for i in range(1, 11):                          # pid 1 every 10 s of a 100 s phase, the shell every 5 s
        t = i * 10.0
        rows.append(_row(t, 3, "systemd", 1, 1, 0.2 * scale)); wakes.append(t - 0.001)
    for i in range(1, 21):
        t = i * 5.0 - 0.5
        rows.append(_row(t, 3, "gnome-shell", 520, 520, 0.5 * scale))
        rows.append(_row(t + 0.1, 3, "llvmpipe-0", 522, 520, 1.0))
    rows.append(_row(50.2, 3, "kworker/3:1", 30, 30, 0.05))       # a per-CPU kernel thread: reported, not gated
    if in_unit:
        rows.append(_row(50.4, 3, "Xwayland", 521, 521, 0.3))     # in the shell's unit, left on the measured CPU
    rows.append(_row(50.6, 0, "snapd", 410, 410, 0.3))            # user space on a harness CPU: nothing
    if foreign_user:
        rows.append(_row(60.0, 3, "snapd", 410, 410, 0.3))        # user space on the measured CPU: the gate
    rows.append(_row(100.0, 0, "perf", 50, 50, 0.01, "R"))
    (d / "perf.steady.timehist.txt").write_text("".join(rows))
    (d / "perf.steady.wakeups.txt").write_text("".join(f"{t:12.6f} [0001]  x[9]  awakened: systemd[1/1]\n" for t in wakes)
                                               + "".join(f"{i * 5.0 - 0.5 - 0.5 * scale / 1000 - 0.001:12.6f} [0001]  x[9]  "
                                                         f"awakened: gnome-shell[520/520]\n" for i in range(1, 21)))
    return d


def test_components_are_per_instance_and_foreign_work_is_split(tmp_path):
    ph = analyze.analyze_run_dir(str(_run_dir(tmp_path / "r1", foreign_user=True, in_unit=True)))["phases"]["steady"]
    sysd = ph["entries"]["systemd"]
    assert set(sysd["threads"]) == {"pid1/systemd"}              # the user manager did not run in this trace
    assert sysd["missing_instances"] == []
    assert sysd["threads"]["pid1/systemd"]["wakes_per_s"] == 0.1
    shell = ph["entries"]["gnome-shell"]
    assert set(shell["threads"]) == {"gnome-shell/gnome-shell"}  # llvmpipe is out (9.5 D15), counted
    assert ph["llvmpipe_rows"] == 20
    f = ph["foreign"]
    assert f["user"]["schedule_ins"] == 1 and set(f["user"]["by_comm"]) == {"snapd"}
    assert f["kernel"]["schedule_ins"] == 1
    assert f["in_unit_other"]["schedule_ins"] == 1
    assert ph["display_servers"] == ["Xwayland"]


def test_the_pool_names_probe_and_foreign_repeats_and_pools_the_rest(tmp_path):
    assert pool.NAME.match("meas-session-session-r3-full")
    assert pool.NAME.match("meas-session-session-r1-probe")
    root = tmp_path / "art"
    for k in range(1, 6):
        _run_dir(root / f"run{k}" / f"meas-session-session-r{k}-full", k=k)
    _run_dir(root / "run6" / "meas-session-session-r6-full", k=6, foreign_user=True)
    _run_dir(root / "run8" / "meas-session-session-r8-full", k=8, in_unit=True)
    _run_dir(root / "run7" / "meas-session-session-r7-probe", k=7, mode="probe")
    _run_dir(root / "run9" / "meas-session-session-r9-dry", k=9, mode="dry")
    runs, gated, other, not_repeats = pool.find_runs(str(root), "EPYC 7763")
    # a dry job runs shortened phases; with the gate open on any model it must not pool as a repeat either
    assert sorted((p["repeat"], p["mode"]) for p in not_repeats) == [(7, "probe"), (9, "dry")]
    # D20: no bound stated, nothing pooled — the pool refuses rather than pooling on an unstated gate
    assert pool.FOREIGN_CPU_SHARE_BOUND is None
    assert pool.pool_app("session", runs["session"])["repeats"] == []
    pool.FOREIGN_CPU_SHARE_BOUND = 1e-6          # the fixture's foreign repeats take 0.3 ms of a 100 s phase
    try:
        entry = pool.pool_app("session", runs["session"])
    finally:
        pool.FOREIGN_CPU_SHARE_BOUND = None
    assert entry["repeats"] == [1, 2, 3, 4, 5]
    # D15: a pinned unit's other process on the measured CPU gates the repeat as user space outside the entries does
    assert [x["repeat"] for x in entry["foreign_user"]] == [6, 8]
    assert all(x["share_of_phase"] > 1e-6 for x in entry["foreign_user"])
    ents = entry["phases"]["steady"]["entries"]
    assert set(ents) == {"gnome-shell", "pipewire", "systemd", "dbus-daemon"}
    # five identical repeats: every value carried holds, each entry on its own components
    q = entry["stability"]["quantities"]
    assert "systemd pid1/systemd wakes/s" in q and "gnome-shell gnome-shell/gnome-shell run mean (ms)" in q
    assert all(c["passes"] for n, c in q.items() if n.startswith(("systemd ", "gnome-shell ")))
    # an entry with nothing observed has nothing to carry, and the rule does not hold for it
    assert q["pipewire (no components)"]["passes"] is False and not entry["stability"]["passes"]


def _probe_dir(d, k, tail_rate, polled_rate=5.0, t0=1000.0, head_s=300.0, tail_s=1200.0, foreign_at=None):
    """A probe job's output: a polled head, then the clean region D19 has the polls stop before.

    The polls' `mono_ns` and the trace share `CLOCK_MONOTONIC`, so the origin is arbitrary and the cut is placed
    from the last poll. gnome-shell's tail rate steps between windows, so a window spread exists to read.
    """
    inst, other = census.instances(PROCS, UID)
    c = {"instances": inst, "in_unit_other": other, "kthreads": [2, 30], "display_servers": []}
    d.mkdir(parents=True, exist_ok=True)
    (d / "report.json").write_text(json.dumps({"app": "session", "repeat": k, "mode": "probe", "gate": "open",
                                               "pin.load_cpu": "3", "edge.idle": "1"}))
    for e in ("start", "end"):
        (d / f"census.idle.{e}.json").write_text(json.dumps(c))
    (d / "edges.jsonl").write_text(json.dumps({"phase": "idle", "edge": "start", "mono_ns": 0}) + "\n")
    (d / "poll.idle.jsonl").write_text("".join(
        json.dumps({"mono_ns": int((t0 + i * 10.0) * 1e9), "session_active": True, "shield_active": True,
                    "power_save_mode": 3}) + "\n" for i in range(int(head_s // 10) + 1)))

    rows, wakes = [_row(t0, 0, "perf", 50, 50, 0.01, "R")], []
    def emit(t, comm, tid, pid):
        rows.append(_row(t, 3, comm, tid, pid, 0.2))
        wakes.append((t - 0.001, comm, tid, pid))
    n = 0
    while n / polled_rate < head_s:                      # the head, as the polls made it
        t = t0 + n / polled_rate
        emit(t, "systemd", 1, 1); emit(t + 0.01, "gnome-shell", 520, 520)
        n += 1
    m, tail0 = 0, t0 + head_s
    while m / tail_rate < tail_s:                        # the clean region; the shell steps every 300 s
        t = tail0 + m / tail_rate
        emit(t, "systemd", 1, 1)
        if int((t - tail0) // 300) % 2 == 0 or m % 2 == 0:
            emit(t + 0.01, "gnome-shell", 520, 520)
        m += 1
    if foreign_at is not None:
        rows.append(_row(tail0 + foreign_at, 3, "snapd", 410, 410, 0.3))
    rows.append(_row(tail0 + tail_s, 0, "perf", 50, 50, 0.01, "R"))
    (d / "perf.idle.timehist.txt").write_text("".join(rows))
    (d / "perf.idle.wakeups.txt").write_text("".join(
        f"{t:12.6f} [0001]  x[9]  awakened: {comm}[{tid}/{pid}]\n" for t, comm, tid, pid in wakes))
    return d


def test_size_steady_reads_only_past_the_last_poll(tmp_path):
    # D19: the polls stop at the steady edge, so the sizing reads the clean region and the polled head is dropped
    a = _probe_dir(tmp_path / "r28", 28, tail_rate=0.5)
    b = _probe_dir(tmp_path / "r29", 29, tail_rate=0.6, foreign_at=700.0)
    res = size_steady.report([str(a), str(b)], margin=60.0, lengths=(300, 600), phase="idle")

    assert [r["cut_s"] for r in res["runs"]] == [360.0, 360.0]        # the last poll at 300 s, a 60 s margin
    assert [r["polls"]["n"] for r in res["runs"]] == [31, 31]
    sysd = res["entries"]["systemd"]
    assert [round(r["mean_wakes_per_s"], 2) for r in sysd["runs"]] == [0.5, 0.6]   # the tail, not the 5.0 head
    assert 12 < sysd["between_sd_pct"] < 14                          # 0.499 against 0.599
    tail = {(b["from_s"], b["to_s"]): b["wakes_per_s"] for b in sysd["poll_tail"]}
    assert tail[(-120, 0)] > 4 and tail[(60, 120)] < 1               # the polled head, then the clean region

    by_len = {r["length_s"]: r for r in sysd["lengths"]}
    assert by_len[300]["windows"] == 6                               # three per run, of the 1140 s left
    assert by_len[300]["total_sd_pct"] >= by_len[300]["between_sd_pct"]
    # one 600 s window per run spreads over nothing, so the length is unread rather than perfect
    assert by_len[600]["windows"] == 0 and by_len[600]["within_sd_pct"] is None and by_len[600]["total_sd_pct"] is None
    # D12: one foreign schedule-in in one 300 s window of one run — five of the six would be pooled
    assert by_len[300]["clean_share"] == 5 / 6
    # the samples a window would hold scale with the length, and the pool reads them per component
    comp = {c["component"]: c for c in sysd["components"]}["pid1/systemd"]
    assert 150 < comp["per_window"][300]["gaps"] < 180 and 300 < comp["per_window"][600]["gaps"] < 360


def _src(repo_root, *p):
    return (repo_root.joinpath("dataset", "tools", "meas", *p)).read_text()


def test_run_sh_carries_the_decisions(repo_root):
    src = _src(repo_root, "session", "run.sh")
    assert "PAMName=login" in src and "XDG_SESSION_TYPE=wayland" in src                 # D11, login mode `unit`
    assert 'LOGIN_MODE="${MEAS_LOGIN_MODE:-gdm}"' in src                                 # D16: GDM's automatic login
    assert "AutomaticLogin=%s" in src and "systemctl restart gdm.service" in src         # D16
    assert "Slice=meas.slice" in src and 'set-property --runtime system.slice AllowedCPUs="$MEAS_HARNESS_CPUS"' in src  # D17
    assert "Delegate=pids memory cpu cpuset" in src                                      # D14
    assert "--headless --virtual-monitor" in src and "VIRTUAL_MONITOR=1920x1080@60" in src
    assert re.search(r"probe \]; then\n\s*PRIMING=1800; STEADY_OFFSET=0; STEADY=10800", src)   # D13
    m = re.search(r"dry \]; then\n\s*PRIMING=(\d+); STEADY_OFFSET=(\d+); STEADY=(\d+)", src)
    assert m and int(m.group(2)) > 310                                                   # D13: past idle-delay + fade
    # D18: the lengths the long-phase probe set — the blank at 304 s, the edge past it
    lens = {k: int(re.search(rf"{k}\(\)\s*{{ echo (\d+); }}", src).group(1))
            for k in ("priming_for", "steady_offset_for")}
    assert lens["steady_offset_for"] > 310 and lens["priming_for"] >= 120, lens
    # D19: the steady length is withdrawn — the polls dominated the signal its spreads were read from — so a full
    # job stops at the no-phase-lengths gate until the unpolled probe sets it
    assert re.search(r"steady_for\(\)\s*{ echo; }", src)
    assert re.search(r'if \[ -z "\$PRIMING" \] \|\| \[ -z "\$STEADY_OFFSET" \] \|\| \[ -z "\$STEADY" \]', src)
    # D21: the system bus restarted into meas.slice before any login, and the placement read from the processes
    # the bus is restarted into meas.slice before the desktop is installed, and every service holding a name on
    # the old bus is restarted with it — without that, logind keeps running nameless and GDM never gets a session
    assert 'sudo systemctl restart "$bus"' in src and "bus_into_meas_slice" in src
    assert src.index("bus_into_meas_slice()") < src.index("install_session() {")
    assert src.index("bus_into_meas_slice\n") < src.index("apt-get install -y ubuntu-desktop-minimal")
    assert 'systemctl show -p BusName --value "$u"' in src and "try-restart" in src
    assert "stop_recorded bus-no-login1" in src
    assert 'CENSUS placed "$OUT/census.pinned.json"' in src and 'CENSUS placed "$OUT/census.edge.json"' in src
    assert src.count("stop_recorded misplaced-entry") == 2
    assert "pin.entry_cgroups" in src and "pin.entry_slices" not in src
    # D19: the probe's polls stop at the steady edge, so the region a full job carries is recorded unpolled
    assert 'poll_start "$name" "${POLL_UNTIL:-}"' in src
    assert 'POLL_UNTIL=$(( LOGIN_T0 + $(steady_offset_for "$APP") ))' in src
    probe_block = src[src.index('if [ "$MODE" = probe ]; then\n  # D19'):]
    assert probe_block.index("POLL_UNTIL=$((") < probe_block.index('phase idle "$STEADY"')
    # D13: the census runs before perf starts and after it stops, never inside the recording
    body = re.search(r"^phase\(\) \{(.*?)^\}", src, re.S | re.M).group(1)
    assert body.index('census "$name.start"') < body.index("perf sched record") < body.index('census "$name.end"')
    # D12: two sweeps, the second at the steady edge before the steady phase
    assert src.index("sweep 1") < src.index("sweep 2") < src.index('phase steady "$STEADY"')


def test_the_loop_knows_the_session_family(repo_root):
    from meas.loop import common
    assert common.FAMILIES["session"]["trigger"] == ".github/campaign-session.json"
    assert "campaign-session.json" in _src(repo_root, "loop", "common.py")
    wf = (repo_root / ".github" / "workflows" / "meas-session.yml").read_text()
    assert "dataset/tools/meas/session/run.sh" in wf and "meas-session-${{ matrix.app }}" in wf
