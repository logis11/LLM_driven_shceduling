"""Constructed cases for the meas-ci instruments and analyzer."""

import json
import subprocess

from meas import analyze, proc_sampler, verify_names


def _stat(pid, comm, utime, stime, threads, starttime):
    fields = ["S", "1", str(pid), str(pid), "0", "-1", "0", "0", "0", "0", "0",
              str(utime), str(stime), "0", "0", "20", "0", str(threads), "0",
              str(starttime)]
    return f"{pid} ({comm}) " + " ".join(fields) + "\n"


def _status(volun, nonvol):
    return (f"Name:\tx\nvoluntary_ctxt_switches:\t{volun}\n"
            f"nonvoluntary_ctxt_switches:\t{nonvol}\n")


def _fake_proc(root, threads):
    """A /proc tree with one process (pid 100) whose threads carry the given
    voluntary counts; /proc/100/status shows the main thread only."""
    pid_dir = root / "100"
    (pid_dir / "task").mkdir(parents=True)
    (pid_dir / "stat").write_text(
        _stat(100, "worker", 250, 30, len(threads), 5000))
    (pid_dir / "status").write_text(_status(threads[100], 1))
    for tid, volun in threads.items():
        (pid_dir / "task" / str(tid)).mkdir()
        (pid_dir / "task" / str(tid) / "status").write_text(_status(volun, 1))
    (root / "meminfo").write_text("MemTotal: 1 kB\n")


def test_sampler_records_every_thread(tmp_path):
    _fake_proc(tmp_path, {100: 5, 101: 40, 102: 7})
    record = proc_sampler.sample(True, proc=str(tmp_path))["procs"][0]
    assert (record["vctxt"], record["threads"]) == (5, 3)
    assert record["tctxt"] == {"100": [5, 1], "101": [40, 1], "102": [7, 1]}


def _write_samples(repeat_dir, samples):
    repeat_dir.mkdir()
    with (repeat_dir / "proc_samples.jsonl").open("w") as out:
        for t_s, procs in samples:
            out.write(json.dumps({"t": t_s * 1_000_000, "procs": procs}) + "\n")


def _proc(ticks, main_volun, tctxt=None):
    proc = {"pid": 100, "starttime": 5000, "comm": "worker", "utime": ticks,
            "stime": 0, "vctxt": main_volun, "nvctxt": 0}
    if tctxt is not None:
        proc["tctxt"] = tctxt
    return proc


def test_wakes_sum_thread_deltas(tmp_path):
    repeat = tmp_path / "r1"
    _write_samples(repeat, [
        (10, [_proc(0, 5, {"100": [5, 0], "101": [40, 0]})]),
        (20, [_proc(10, 6, {"100": [6, 0], "101": [60, 0], "102": [3, 0]})]),
    ])
    (entry,) = analyze.wake_stats(repeat, (0, 86_399), lambda c: c == "worker")
    assert entry["wakes"] == 1 + 20  # thread 102 appeared once: no delta
    assert entry["work_us"] == 10 * analyze.TICK_US / 21
    assert analyze.has_thread_ctxt(repeat)


def test_wakes_fall_back_to_main_thread(tmp_path):
    repeat = tmp_path / "r1"
    _write_samples(repeat, [(10, [_proc(0, 5)]), (20, [_proc(10, 15)])])
    (entry,) = analyze.wake_stats(repeat, (0, 86_399), lambda c: c == "worker")
    assert entry["wakes"] == 10
    assert not analyze.has_thread_ctxt(repeat)


def test_wake_stats_pid_filter(tmp_path):
    repeat = tmp_path / "r1"
    _write_samples(repeat, [(10, [_proc(0, 5)]), (20, [_proc(10, 15)])])
    assert analyze.wake_stats(repeat, (0, 86_399), lambda c: True,
                              pids={999}) == []


def test_lognormal_fit_reports_zeros():
    fit = analyze.lognormal_fit([0, 0, 100, 200, 400])
    assert (fit["n"], fit["median_us"], fit["p90_us"]) == (3, 200, 400)
    assert (fit["n_nonpositive"], fit["median_all_us"]) == (2, 100)
    assert "n_nonpositive" not in analyze.lognormal_fit([100, 200, 400])


LIFECYCLE = """\
Time     Event     PID Info   Duration Process
00:00:10 fork     3775 parent          make -C /tmp/linux-6.6 -j8
00:00:10 fork     3776 child           make -C /tmp/linux-6.6 -j8
00:00:11 fork     3776 parent          /bin/sh -c gcc -c foo.c
00:00:11 fork     3777 child           /bin/sh -c gcc -c foo.c
00:00:12 fork     3790 parent          /usr/bin/make -f ./scripts/Makefile.build obj=init
00:00:12 fork     3791 child           /usr/bin/make -f ./scripts/Makefile.build obj=init
00:00:40 fork     3775 parent          make -C /tmp/linux-6.6 -j8
00:00:40 fork     3799 child           make -C /tmp/linux-6.6 -j8
00:00:15 exit     4001      0   0.350s /snap/chromium/current/usr/lib/chromium-browser/chrome --type=renderer --renderer-client-id=6
00:00:16 comm     4010                 /snap/chromium/current/usr/lib/chromium-browser/chrome --type=zygote
00:00:17 exit     4020      0   9.000s /snap/chromium/current/usr/lib/chromium-browser/chrome --type=renderer --renderer-client-id=5
"""


def test_forks_counted_by_parent_only(tmp_path):
    repeat = tmp_path / "r1"
    repeat.mkdir()
    (repeat / "lifecycle.log").write_text(LIFECYCLE)
    # make's own forks inside the window; the shell's fork of gcc is not make's
    assert analyze.count_forks_by(repeat, (10, 30), {"make"}) == 2


def test_renderer_pids_from_lifecycle(tmp_path):
    repeat = tmp_path / "r1"
    repeat.mkdir()
    (repeat / "lifecycle.log").write_text(LIFECYCLE)
    assert analyze.pids_with_arg(repeat, (10, 30), "--type=renderer") == {4001, 4020}


def test_name_level_needs_the_catalog_name():
    gcc_only = {"gcc": "gcc -O2 -c /tmp/probe.c"}
    assert verify_names.decide_level("cc1", ["/usr/bin/gcc"], gcc_only) == "binary-only"
    cc1 = {"cc1": "/usr/libexec/gcc/x86_64-linux-gnu/13/cc1 -quiet probe.c"}
    assert verify_names.decide_level("cc1", ["/usr/bin/gcc"], cc1) == "runtime"
    assert verify_names.decide_level("cc1", [], {"error": "ENOENT"}) == "package-no-binary"
    assert verify_names.decide_level("borg", [], None) == "package-no-binary"


def test_name_level_matches_truncated_comm():
    truncated = {"tracker-miner-f": "/usr/libexec/tracker-miner-fs-3"}
    assert verify_names.name_observed("tracker-miner-fs-3", truncated)
    assert verify_names.name_observed("tracker-miner-fs-3",
                                      {"tracker-miner-f": ""})
    assert not verify_names.name_observed("tracker-miner-fs-3",
                                          {"tracker-extract": ""})


def test_snap_stub_is_not_a_binary(tmp_path):
    stub = tmp_path / "thunderbird"
    stub.write_text("#!/bin/sh\necho 'install the snap: snap install thunderbird'\n")
    elf = tmp_path / "rsync"
    elf.write_bytes(b"\x7fELF\x02\x01\x01")
    assert verify_names.is_snap_stub(stub)
    assert not verify_names.is_snap_stub(elf)


def test_package_binaries_include_sbin(monkeypatch):
    listing = "/.\n/usr/sbin/dkms\n/usr/share/man/man8/dkms.8.gz\n/usr/lib/dkms/common.postinst\n"
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
        a, 0, stdout=listing, stderr=""))
    assert verify_names.package_binaries("ubuntu", "dkms") == [
        "/usr/sbin/dkms", "/usr/lib/dkms/common.postinst"]


# ---- campaign analyzer: the wake definition (9.5 follow-ups spec, decision 4) ----

import pytest  # noqa: E402
from meas.campaign import analyze as campaign  # noqa: E402
from meas.build import analyze as build  # noqa: E402


def _row(t_in, run_ms, tid=7, comm="app"):
    return campaign.Row(t_in, t_in, t_in + run_ms / 1000, run_ms, comm, tid, 100)


def _bseg(t_in, run_ms, state, tid=7, comm="app"):
    return build.Seg(t_in, t_in, t_in + run_ms / 1000, run_ms, comm, tid, 100, state, 3)


def test_resume_after_preemption_extends_the_preceding_wake():
    # one thread: woken at 1.000, runs 2 ms, preempted, resumes at 1.0025 for 1 ms
    # with no wakeup in between; then sleeps, is woken at 1.0095 and runs 0.5 ms
    rows = [_row(1.000, 2.0), _row(1.0025, 1.0), _row(1.010, 0.5)]
    wakeups = {7: [0.9999, 1.0095]}
    wakes, merged = campaign.merge_resumes(rows, wakeups)
    assert merged == 1
    got = [x for w in wakes for x in (w.t_in, w.run, w.t_end)]
    assert got == pytest.approx([1.000, 3.0, 1.0035, 1.010, 0.5, 1.0105])


def test_a_waking_row_before_the_switch_out_still_makes_a_wake():
    # a 3 µs run that blocks on a ~7 µs I/O wait: the waker's sched_waking fires at 1.000002, while the thread is
    # still switching out (recorded at 1.000003); it fires only for a thread already in a sleep state (kernel
    # try_to_wake_up: trace_sched_waking after ttwu_state_match), so it wakes the sleep that follows
    rows = [_row(1.000, 0.003), _row(1.000010, 0.003)]
    wakes, merged = campaign.merge_resumes(rows, {7: [0.9999, 1.000002]})
    assert merged == 0 and len(wakes) == 2
    wakes, merged = build.merge_resumes([_bseg(1.000, 0.003, "D"), _bseg(1.000010, 0.003, "S")], {7: [0.9999, 1.000002]})
    assert merged == 0 and len(wakes) == 2


def test_the_switch_out_state_decides_where_it_was_recorded():
    # 9.7 D21: S or D before the gap is a wake, R a resume, whatever the rows say; the disagreements are counted
    check = {}
    segs = [_bseg(1.000, 0.003, "S"), _bseg(1.000010, 0.003, "R"), _bseg(1.000020, 0.003, "D"), _bseg(1.000030, 0.003, "S")]
    wakes, merged = build.merge_resumes(segs, {7: [1.000015, 1.000026]}, check)
    # gap 1 (after S, no row): a wake; gap 2 (after R, a row at 1.000015): a resume; gap 3 (after D, a row): a wake
    assert [w.t_in for w in wakes] == [1.000, 1.000010, 1.000030] and merged == 1
    assert check == {"slept_without_row": 1, "preempted_with_row": 1}
    wakes, merged = build.merge_resumes([s._replace(state="") for s in segs], {7: [1.000015, 1.000026]})
    assert [w.t_in for w in wakes] == [1.000, 1.000020, 1.000030]   # no state recorded: the rows decide


def test_a_row_before_the_last_schedule_in_belongs_to_the_earlier_sleep():
    rows = [_row(1.000, 0.003), _row(1.000010, 0.003)]
    wakes, merged = campaign.merge_resumes(rows, {7: [0.999999]})   # woke the first segment, not the second
    assert merged == 1


def test_first_row_without_a_wakeup_in_the_capture_is_a_wake():
    rows = [_row(1.000, 2.0), _row(1.005, 1.0)]
    wakes, merged = campaign.merge_resumes(rows, {})  # no wakeups file rows for this thread
    assert merged == 1 and len(wakes) == 1 and wakes[0].run == 3.0


def test_threads_are_merged_independently():
    rows = sorted([_row(1.000, 2.0, tid=7), _row(1.001, 1.0, tid=8), _row(1.0025, 1.0, tid=7)], key=lambda r: r.t_in)
    wakes, merged = campaign.merge_resumes(rows, {7: [0.9999], 8: [1.0009]})
    assert merged == 1
    assert sorted((w.tid, w.run) for w in wakes) == [(7, 3.0), (8, 1.0)]


def test_the_row_decides_and_the_state_checks_it():
    # 9.5 D39: the campaign keeps the row window for every repeat; a recorded switch-out state only counts where the
    # row disagrees with it, per comm, and a folded resume carries its own switch-out state into the wake
    check = {}
    rows = [_row(1.000, 0.003)._replace(state="S"), _row(1.000010, 0.003)._replace(state="R"),
            _row(1.000020, 0.003)._replace(state="D"), _row(1.000030, 0.003)._replace(state="S")]
    wakes, merged = campaign.merge_resumes(rows, {7: [1.000015, 1.000026]}, check)
    # gap 1 (after S, no row): folded by the row; gap 2 (after R, a row): a wake by the row; gap 3 (after D, a row): a wake
    assert [w.t_in for w in wakes] == [1.000, 1.000020, 1.000030] and merged == 1
    assert wakes[0].state == "R"
    assert check == {"app": {"gaps": 3, "slept_without_row": 1, "preempted_with_row": 1}}
    check = {}
    campaign.merge_resumes([r._replace(state="") for r in rows], {7: [1.000015, 1.000026]}, check)
    assert check == {}   # no state recorded (the campaign's earlier repeats): nothing to check


def test_timehist_rows_with_and_without_the_state_column(tmp_path):
    p = tmp_path / "perf.idle.timehist.txt"
    p.write_text("           time    cpu  task name                       wait time  sch delay   run time  state\n"
                 "   1.000300 [0003]  vo[7/100]    0.000      0.004      0.300      S\n"
                 "   1.000900 [0003]  vo[7/100]    0.100      0.002      0.200\n")
    rows, _, _ = campaign.load_rows(str(p), {100})
    assert [(r.comm, r.tid, r.run, r.state) for r in rows] == [("vo", 7, 0.3, "S"), ("vo", 7, 0.2, "")]


def test_all_wakeups_indexed_by_wakee_tid(tmp_path):
    p = tmp_path / "perf.idle.wakeups.txt"
    p.write_text("   1.000500 [0001]  Xvfb[500]  awakened: app[7/100]\n"
                 "   1.000600 [0002]  app[8/100]  awakened: app[7/100]\n"
                 "   1.000700 [0002]  other[9/200]  awakened: other[9/200]\n")
    assert campaign.load_all_wakeups(str(p), {100}) == {7: [1.0005, 1.0006]}


# ---- campaign analyzer: operation windows (9.5 follow-ups spec, decisions 8–9) ----

def test_operation_windows_cut_rows_and_measure_duration():
    ops = [{"op": "x", "i": 0, "trigger_us": 1_000_000, "done_us": 1_200_000, "rc": 0},
           {"op": "x", "i": 1, "trigger_us": 2_000_000, "done_us": 2_050_000, "rc": 2},   # failed: excluded
           {"op": "x", "i": 2, "trigger_us": 3_000_000, "done_us": 3_400_000, "rc": 0}]
    rows = [_row(0.5, 1.0), _row(1.05, 2.0), _row(1.10, 3.0), _row(2.01, 1.0), _row(3.1, 5.0), _row(3.5, 1.0)]
    res = campaign.operation_windows(rows, ops)
    assert res["durations_ms"] == [200.0, 400.0]
    assert res["n_ok"] == 2 and res["n_failed"] == 1
    assert [r.t_in for r in res["inside"]] == [1.05, 1.10, 3.1]
    assert [r.t_in for r in res["outside"]] == [0.5, 2.01, 3.5]
