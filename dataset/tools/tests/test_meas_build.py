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


from meas.build import analyze as build  # noqa: E402
from meas.build import shapes  # noqa: E402


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


def test_blocks_after_runs_are_zero_when_another_thread_runs_on():
    rows = [build.Seg(1.000, 1.000, 1.004, 4.0, "p", 7, 1, "S", 3),    # 7 sleeps; 8 is runnable: block 0
            build.Seg(1.004, 1.003, 1.006, 2.0, "p", 8, 1, "R", 3),
            build.Seg(1.009, 1.009, 1.010, 1.0, "p", 8, 1, "S", 3),    # 8 sleeps; nothing until 1.015: block 5 ms
            build.Seg(1.015, 1.015, 1.016, 1.0, "p", 7, 1, "Z", 3)]
    assert shapes.blocks_after_runs(rows, 1.000, 1.016) == pytest.approx([0.0, 5.0])


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
    assert b["_samples"]["blocks_after_runs_ms"] == pytest.approx([0.2, 0.3])
    assert b["mean_block_ms"] == pytest.approx(0.25)
    assert b["job_s"] == pytest.approx(0.0215, abs=1e-6)
    cut = build.batch("clamscan", tree, tid2pid, role, segs, {}, 3, recs, 0.03, job_end=1.0203)
    assert cut["job_s"] == pytest.approx(0.0203, abs=1e-6) and cut["_samples"]["runs_between_blocks_ms"] == pytest.approx([12.0, 8.0])


from meas.build import pool  # noqa: E402


def test_criterion_lists_every_carried_value():
    def rp(*v):
        return {"repeat_mean": dict(zip((4, 5, 7, 8, 9), v))}
    out = {"phases": {
        "build-j8-warm": {"roles": {n: {"cpu_per_process_us": rp(100, 101, 100, 102, 101)} for n in pool.CRITERION_ROLES},
                          "dispatch": {"per_dispatch_us": rp(670, 675, 673, 681, 676)},
                          "object_members": {"step_cpu_us": {"sh 1/4": rp(726, 785, 752, 785, 760)}}},
        "ffmpeg": {"shape": {"runs_between_blocks_us": rp(7, 7, 6, 6, 7),
                             "mean_block_us": dict(zip((4, 5, 7, 8, 9), (0.43, 0.29, 0.26, 0.26, 0.3))),
                             "share_past_boot_slice": dict(zip((4, 5, 7, 8, 9), (0.702, 0.698, 0.696, 0.704, 0.700)))}}}}
    crit = pool.criterion(out)
    assert set(crit) == {f"{n} CPU per process" for n in pool.CRITERION_ROLES} | {
        "make dispatch", "object-job sh 1/4", "ffmpeg run between blocks", "ffmpeg mean block per run",
        "ffmpeg share past the boot slice"}
    assert crit["ffmpeg run between blocks"]["passes"] is True        # within the 1 µs floor
    assert crit["ffmpeg mean block per run"]["passes"] is True        # sub-µs mean, within the floor
    assert all(c["k"] == 5 for c in crit.values())
    four = {"phases": {"ffmpeg": {"shape": {"runs_between_blocks_us": rp(7, 7, 7, 7), "mean_block_us": {4: 0.3, 5: 0.3, 7: 0.3, 8: 0.3},
                                            "share_past_boot_slice": {4: 0.7, 5: 0.7, 7: 0.7, 8: 0.7}}}}}
    assert not any(c["passes"] for c in pool.criterion(four).values())    # four repeats: below the minimum
    assert all(c["needed"] is None or c["needed"] >= 5 for c in crit.values())


def test_pooled_carries_the_per_repeat_mean_and_the_rule_reads_it():
    # D26: a carried table is tested by its per-repeat mean — the medians agree, the means do not
    t = pool.pooled({4: [1.0, 2.0, 3.0], 5: [1.0, 2.0, 3.6], 7: [1.0, 2.0, 3.0], 8: [1.0, 2.0, 3.6], 9: [1.0, 2.0, 3.0]}, 1000.0)
    assert t["repeat_p50"] == {4: 2000.0, 5: 2000.0, 7: 2000.0, 8: 2000.0, 9: 2000.0}
    assert t["repeat_mean"] == pytest.approx({4: 2000.0, 5: 2200.0, 7: 2000.0, 8: 2200.0, 9: 2000.0})
    out = {"phases": {"build-j8-warm": {"roles": {}, "object_members": {"step_cpu_us": {"sh 1/4": t}}}}}
    c = pool.criterion(out)["object-job sh 1/4"]
    assert c["mean"] == pytest.approx(2080.0) and c["passes"] is False    # ±6.5 %: the medians alone would pass
    assert c["needed"] == 7


def test_repeats_needed_is_at_least_five_and_follows_the_spread():
    assert pool.repeats_needed({4: 100.0, 5: 100.0, 7: 100.0, 8: 100.0}) == 5
    assert pool.repeats_needed({4: 0.3, 5: 0.5, 7: 0.2, 8: 0.4}, abs_floor=1.0) == 5     # within the 1 µs floor
    wide = pool.repeats_needed({4: 196.0, 5: 233.0, 7: 205.0, 8: 220.0}, abs_floor=1.0)
    assert wide > 5 and pool.repeats_needed({4: 196.0, 5: 233.0, 7: 205.0, 8: 220.0}) == wide
    assert pool.repeats_needed({4: 100.0}) is None


def test_clamav_daily_reads_the_fixed_copy_or_the_version_line():
    # D27: repeats 4-8 read daily 28127, repeat 9 on the fixed 28128
    assert pool.clamav_daily({"clamav.db": "ClamAV 1.5.3/28127/Fri Sep 18 06:25:28 2026"}) == "28127"
    assert pool.clamav_daily({"clamav.db": "ClamAV 1.5.3/28128/Sat Sep 19 06:24:24 2026", "clamav.db.daily": "28128"}) == "28128"
    assert pool.clamav_daily({"clamav.db": "none: MEAS_CLAMAV_DB unset, clamscan not run (D27)"}) is None
    assert pool.clamav_daily({}) is None


def test_not_pooled_names_the_database_and_the_warm_start():
    # D27: clamscan on another signature database; D28: python3 without its warm-up run, or after a failed one
    assert pool.not_pooled("clamscan", "28127", None) == "signature database daily 28127"
    assert pool.not_pooled("clamscan", pool.CLAMAV_DAILY, None) is None
    assert pool.not_pooled("train", "28127", None) == "no warm-up run"
    assert pool.not_pooled("train", "28127", "1") == "warm-up run rc 1"
    assert pool.not_pooled("train", None, "0") is None
    assert pool.not_pooled("ffmpeg", "28127", None) is None
