"""Constructed cases for the launch subjects of the desktop family (9.10 changelog D132–D135)."""

import gzip
import json
import re

from meas.desktop import launch


def _gz(path, text):
    with gzip.open(path, "wt") as f:
        f.write(text)


def _row(t_out, cpu, comm, tid, pid, run_ms, state="S", delay_ms=0.0):
    return f"{t_out:15.6f} [{cpu:04d}]  {comm}[{tid}/{pid}]  0.000  {delay_ms:.3f}  {run_ms:.3f}  {state}\n"


def _edges(D, *rows):
    (D / "launch-edges.jsonl").write_text("".join(json.dumps({"phase": p, "edge": e, "mono_ns": int(t * 1e9)}) + "\n"
                                                  for p, e, t in rows))


def _kv(D, **kv):
    (D / "report.kv").write_text("".join(f"{k.replace('_', '.') if k.startswith('launch_') else k}={v}\n"
                                         for k, v in kv.items()))


def test_a_traced_launch_from_the_applications_exec_to_the_settles_end(tmp_path):
    D = tmp_path
    # run.sh (pid 50) forks the launch (100), which execs taskset, setsid and bash before LibreOffice's launcher;
    # 100 forks soffice.bin (101), which starts a thread (102)
    _gz(D / "perf.launch.forks.txt.gz",
        "      10.000000: sched:sched_process_fork: comm=bash pid=50 child_comm=bash child_pid=100\n"
        "      10.001000: sched:sched_process_exec: filename=/usr/bin/taskset pid=100 old_pid=100\n"
        "      10.002000: sched:sched_process_exec: filename=/usr/bin/setsid pid=100 old_pid=100\n"
        "      10.003000: sched:sched_process_exec: filename=/usr/bin/bash pid=100 old_pid=100\n"
        "      10.004000: sched:sched_process_exec: filename=/usr/bin/soffice pid=100 old_pid=100\n"
        "      10.100000: sched:sched_process_fork: comm=oosplash pid=100 child_comm=oosplash child_pid=101\n"
        "      10.200000: sched:sched_process_fork: comm=soffice.bin pid=101 child_comm=soffice.bin child_pid=102\n")
    _gz(D / "perf.launch.timehist.txt.gz",
        _row(10.0008, 0, "bash", 100, 100, 0.5)                    # the launch chain before the exec: not the phase
        + _row(10.0500, 3, "oosplash", 100, 100, 40.0)             # wake 1 (10.010 in)
        + _row(10.3000, 3, "soffice.bin", 101, 101, 100.0, "R")    # wake 2, preempted
        + _row(10.3500, 3, "soffice.bin", 101, 101, 20.0)          # its resume, merged into wake 2
        + _row(12.0000, 3, "soffice.bin", 102, 101, 5.0)           # wake 3, the thread
        + _row(13.0000, 3, "Runner.Worker", 900, 900, 2.0)         # on the measured CPU, outside the tree
        + _row(26.0000, 3, "soffice.bin", 101, 101, 7.0))          # past the settle's end
    _gz(D / "perf.launch.wakeups.txt.gz",
        "      11.990000 [0001]  swapper[0]  awakened: soffice.bin[102/101]\n")
    _edges(D, ("traced.exec", "mark", 9.9), ("traced.settle", "end", 25.0))
    (D / "report.kv").write_text("app=launch-soffice\nrepeat=1\nmode=dry\nlaunch.traced.root=100\npin.load_cpu=3\n")
    out, events = launch.analyze(str(D))
    assert out["start"] == "exec of /usr/bin/soffice"
    assert out["phase_s"] == round(25.0 - 10.004, 3)
    assert out["wakes"] == 3 and out["resumes_merged"] == 1
    assert out["cpu_ms"] == 40.0 + 120.0 + 5.0
    assert out["outside"] == {"Runner.Worker": {"rows": 1, "run_ms": 2.0}}
    slices = out["streams"]["tree"]["slices"]
    assert len(slices["cpu_ms_per_s"]) == 2          # 14.996 s in 10 s slices, the last one short
    assert slices["cpu_ms_per_s"][0] == round(165.0 / 10, 3)
    # each wake's time from the exec
    assert [e[1] for e in events] == [round((10.0100 - 10.004) * 1e6), round((10.2000 - 10.004) * 1e6),
                                       round((11.9950 - 10.004) * 1e6)]
    launch.write(str(D), out, events)
    assert (D / "launch.events.tsv.gz").exists() and json.load(open(D / "launch.summary.json"))["wakes"] == 3
    assert "launch.wakes=3" in launch.keys(out)


def test_the_call_is_the_running_browsers_threads_and_their_descendants_from_the_opening(tmp_path):
    D = tmp_path
    (D / "launch.seed.tsv").write_text("500\t500\tchrome\n500\t501\tThreadPoolForeg\n")
    _gz(D / "perf.launch.forks.txt.gz",
        "      20.500000: sched:sched_process_fork: comm=chrome pid=501 child_comm=chrome child_pid=600\n")
    _gz(D / "perf.launch.timehist.txt.gz",
        _row(19.5000, 3, "chrome", 500, 500, 1.0)                 # before the opening
        + _row(21.0000, 3, "chrome", 500, 500, 2.0)
        + _row(22.0000, 3, "AudioWorkerThre", 600, 600, 3.0)      # the call's process, forked after the opening
        + _row(23.0000, 3, "chrome", 700, 700, 4.0))              # another chrome, not the browser's
    _gz(D / "perf.launch.wakeups.txt.gz", "")
    _edges(D, ("traced.call", "open", 20.0), ("traced.settle", "end", 30.0))
    (D / "report.kv").write_text("app=launch-webrtc\nrepeat=2\nmode=dry\npin.load_cpu=3\n")
    out, _ = launch.analyze(str(D))
    assert out["start"] == "the call's opening" and out["phase_s"] == 10.0
    assert out["wakes"] == 2 and out["cpu_ms"] == 5.0
    assert out["outside"] == {"chrome": {"rows": 1, "run_ms": 4.0}}


def test_the_hidden_tabs_renderers_are_streams_of_their_own_the_control_tab_dropped(tmp_path):
    D = tmp_path
    (D / "launch.renderers.traced.tsv").write_text(
        "201\t/opt/google/chrome/chrome --type=renderer --renderer-client-id=5\n"
        "202\t/opt/google/chrome/chrome --type=renderer --renderer-client-id=6\n"
        "203\t/opt/google/chrome/chrome --type=renderer --renderer-client-id=7\n"
        "204\t/opt/google/chrome/chrome --type=renderer --extension-process --renderer-client-id=8\n")
    forks = "      10.000000: sched:sched_process_exec: filename=/opt/google/chrome/chrome pid=100 old_pid=100\n"
    forks += "".join(f"      10.1{k}0000: sched:sched_process_fork: comm=chrome pid=100 child_comm=chrome child_pid={p}\n"
                     for k, p in enumerate((201, 202, 203, 204)))
    _gz(D / "perf.launch.forks.txt.gz", forks)
    rows = "".join(_row(11.0 + i * 0.1, 3, "chrome", 201, 201, 1.0) for i in range(10))   # the selected tab: fastest
    rows += _row(12.0, 3, "chrome", 202, 202, 2.0) + _row(13.0, 3, "chrome", 203, 203, 3.0)
    rows += _row(14.0, 3, "chrome", 204, 204, 9.0)                                          # an extension renderer
    _gz(D / "perf.launch.timehist.txt.gz", rows)
    _gz(D / "perf.launch.wakeups.txt.gz", "")
    _edges(D, ("traced.settle", "end", 20.0))
    (D / "report.kv").write_text("app=launch-chrome-hidden\nrepeat=1\nlaunch.traced.root=100\npin.load_cpu=3\n")
    out, events = launch.analyze(str(D))
    assert out["page_renderers"] == 3 and out["control_tab"]["pid"] == 201
    assert sorted(k for k in out["streams"] if k != "tree") == ["renderer1", "renderer2"]
    assert out["streams"]["renderer1"]["cpu_ms"] == 2.0 and out["streams"]["renderer2"]["cpu_ms"] == 3.0
    assert {e[0] for e in events} == {"tree", "renderer1", "renderer2"}
    # the gate's listing names the tabs' renderers: one started later in the grace hosts no tab (dry run #80)
    (D / "launch.renderers.traced.gate.tsv").write_text(
        "201\t/opt/google/chrome/chrome --type=renderer --renderer-client-id=5\n"
        "202\t/opt/google/chrome/chrome --type=renderer --renderer-client-id=6\n")
    out, _ = launch.analyze(str(D))
    assert out["late_renderers"] == [203] and sorted(k for k in out["streams"] if k != "tree") == ["renderer1"]


def test_the_live_tree_is_the_roots_session_and_its_descendants():
    table = {100: (1, 100, "soffice", []), 101: (100, 100, "oosplash", []),
             102: (1, 100, "dbus-daemon", []),        # daemonised, still in the session
             103: (101, 103, "soffice.bin", []),      # its own session, below the root
             104: (1, 104, "Xvfb", [])}
    assert launch.live_tree(100, table) == [100, 101, 102, 103]
    assert launch.SESSION.match("dbus-daemon") and not launch.SESSION.match("soffice.bin")


def test_the_mapped_files_are_the_regular_files_a_process_maps(tmp_path):
    (tmp_path / "100").mkdir()
    (tmp_path / "100" / "maps").write_text(
        "7f00-7f01 r-xp 00000000 08:01 1234 /usr/lib/libreoffice/program/soffice.bin\n"
        "7f01-7f02 r--p 00000000 08:01 1235 /usr/lib/x86_64-linux-gnu/libc.so.6\n"
        "7f02-7f03 rw-p 00000000 00:00 0 \n"
        "7f03-7f04 rw-p 00000000 00:00 0 [heap]\n"
        "7f04-7f05 rw-s 00000000 00:05 77 /dev/shm/.org.chromium.x\n"
        "7f05-7f06 r--p 00000000 08:01 88 /tmp/gone (deleted)\n"
        "7f06-7f07 r--p 00000000 08:01 1234 /usr/lib/libreoffice/program/soffice.bin\n")
    assert launch.mapped_files([100], proc=str(tmp_path)) == [
        "/usr/lib/libreoffice/program/soffice.bin", "/usr/lib/x86_64-linux-gnu/libc.so.6"]


def test_the_pool_sets_the_repeats_side_by_side(tmp_path):
    for k, (cpu, sl) in enumerate(((100.0, [8.0, 2.0]), (120.0, [10.0, 2.0, 0.5])), start=1):
        d = tmp_path / f"r{k}"
        d.mkdir()
        json.dump({"subject": "launch-kdenlive", "repeat": str(k), "version": "Kdenlive 23.08.5", "phase_s": 15.0 + k,
                   "cpu_ms": cpu, "wakes": 10 * k, "streams": {"tree": {"slices": {"cpu_ms_per_s": sl}}}},
                  open(d / "launch.summary.json", "w"))
    e = launch.pool([str(tmp_path / "r1"), str(tmp_path / "r2")])["launch-kdenlive"]
    assert e["repeats"] == ["1", "2"] and e["cpu_ms"] == [100.0, 120.0]
    assert e["slice_cpu_ms_per_s_mean"] == [9.0, 2.0]    # over the slices every repeat has


def test_each_subjects_settle_is_its_campaigns(repo_root):
    # D133: the launch phase ends where the entry's steady values began — 9.5's settle_for, 9.8's launch-settle
    meas = repo_root / "dataset" / "tools" / "meas"
    sh = (meas / "desktop" / "launch.sh").read_text()
    body = sh[sh.index("ln_settle_for() {"):]
    body = body[:body.index("\n}\n")]
    ours = {}
    for names, val in re.findall(r"^\s*([a-z0-9|-]+)\) echo \"?([0-9A-Z_$]+)\"? ;;", body, re.M):
        for n in names.split("|"):
            ours[n] = val
    run95 = (meas / "campaign" / "run.sh").read_text()
    s95 = run95[run95.index("settle_for() {"):]
    s95 = s95[:s95.index("\n}\n")]
    theirs = {}
    for names, val in re.findall(r"^\s*([a-z0-9|-]+)\) echo ([0-9]+) ;;", s95, re.M):
        for n in names.split("|"):
            theirs[n] = val
    for arm in ("soffice", "thunderbird-send", "kdenlive", "mpv-video", "mpv-audio", "chrome", "webrtc"):
        assert ours[arm] == theirs[arm], arm
    desk = (meas / "desktop" / "run.sh").read_text()
    assert re.search(r"chrome-hidden\|chrome-visible\|chrome-tabs\|element\) echo 20 ;;", desk)
    assert ours["chrome-hidden"] == "20" and "LN_GRACE=630" in sh
    assert re.search(r"steam\) echo 900 ;;", desk) and ours["steam"] == "900"
    # Element: 9.8's 30 s after the sign-in and its 20 s launch-settle (D135)
    assert ours["element"] == "$LN_ELEMENT_SETTLE" and "LN_ELEMENT_SETTLE=50" in sh
    assert "sleep 30; screenshot after-login" in desk


def test_a_launch_dry_run_keeps_the_campaigns_lengths(repo_root):
    # D135: the dry run reads the form's question, so it runs the campaign's lengths; run.sh's dry block skips launch-*
    src = (repo_root / "dataset" / "tools" / "meas" / "desktop" / "run.sh").read_text()
    assert re.search(r'^if \[ "\$MODE" = dry \] && \[ "\$\{APP#launch-\}" = "\$APP" \]; then', src, re.M)
    assert 'launch-*) launch_subject "${APP#launch-}" ;;' in src


def test_the_fold_in_carries_each_streams_wakes_with_its_threads(tmp_path):
    from meas.desktop import launch_fold_in
    D = tmp_path
    json.dump({"phase_s": 12.3456789, "streams": {"tree": {}, "renderer2": {}, "renderer1": {}}},
              open(D / "launch.summary.json", "w"))
    with gzip.open(D / "launch.events.tsv.gz", "wt") as f:
        f.write("stream\tt_us\trun_us\ttid\tpid\tcomm\trole\n"
                "renderer1\t500\t20\t11\t11\tchrome\trenderer\n"
                "renderer2\t100\t30\t12\t12\tchrome\trenderer\n"
                "renderer1\t200\t10\t13\t11\tHangWatcher\trenderer\n"
                "tree\t0\t99\t1\t1\tchrome\tchrome\n")
    phase, streams, comms = launch_fold_in.streams_of(str(D), "chrome-hidden")
    assert phase == 12_345_679
    assert comms == ["chrome", "HangWatcher"]
    # the renderers in their index order, each sorted by time; the tree's stream is not a renderer's
    assert streams == [[[200, 10, 1], [500, 20, 0]], [[100, 30, 0]]]
    phase, streams, _ = launch_fold_in.streams_of(str(D), "soffice")
    assert streams == [[[0, 99, 0]]]
    # byte-stable: the same document encodes to the same bytes
    doc = {"repeats": [{"phase_us": phase, "streams": streams}]}
    assert launch_fold_in.encode(doc) == launch_fold_in.encode(doc)
