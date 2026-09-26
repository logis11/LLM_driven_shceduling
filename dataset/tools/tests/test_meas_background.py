"""Constructed cases for the 9.7 background campaign's tools (campaign/method.md §2, §5; changelog D6, D7, D12–D15)."""

import gzip
import json

import pytest

from meas.background import analyze, appinfo, fileset, nettrace, pool

Seg = analyze._build.Seg


# ---- nettrace: decoding the recorded calls --------------------------------------

def _pairs(*calls):
    """(t0, t1, pid, tid, nr, args, ret) tuples from (t0, t1, nr, args, ret) with pid 200, tid 201."""
    return [(t0, t1, 200, 201, nr, tuple(args), ret) for t0, t1, nr, args, ret in calls]


def test_64bit_calls_follow_the_descriptor_table():
    calls, unknown = nettrace.decode(_pairs(
        (1.0, 1.1, 41, (2, 1, 0), 5),        # socket -> 5
        (1.2, 1.3, 42, (5, 0, 16), 0),       # connect(5)
        (1.4, 1.5, 0, (5, 0, 4096), 1448),   # read(5): a socket receive
        (1.6, 1.7, 0, (7, 0, 4096), 4096),   # read(7): a file read
        (1.8, 1.9, 3, (5,), 0),              # close(5)
        (2.0, 2.1, 0, (5, 0, 4096), 10),     # read(5) after close: a file read
        (2.2, 2.3, 1, (5, 0, 10), 10),       # write(5): a file write
    ))
    assert [(c.name, c.kind) for c in calls] == [("socket", "socket"), ("connect", "connect"), ("read", "recv"),
                                                  ("read", "fread"), ("close", "close"), ("read", "fread"), ("write", "fwrite")]
    assert calls[2].nbytes == 1448 and calls[3].nbytes is None and unknown == {}


def test_32bit_calls_use_the_i386_table_and_socketcall():
    calls, unknown = nettrace.decode(_pairs(
        (1.0, 1.1, 102, (1, 0xffd0), 6),      # socketcall(SYS_SOCKET) -> 6
        (1.2, 1.3, 102, (10, 0xffd0), 1448),  # socketcall(SYS_RECV): a socket receive, descriptor unknown
        (1.4, 1.5, 3, (6, 0, 4096), 512),     # i386 read(6): a socket receive
        (1.6, 1.7, 45, (0,), 0x1000),         # i386 45 is brk: not a method call
        (1.8, 1.9, 371, (6, 0, 4096), 99),    # i386 recvfrom
        (2.0, 2.1, 168, (0, 1, 1000), 1),     # i386 poll
    ), compat_pids=[200])
    assert [(c.name, c.kind, c.fd) for c in calls] == [("socket", "socket", None), ("recv", "recv", None),
                                                        ("read", "recv", 6), ("recvfrom", "recv", 6), ("poll", "poll", 0)]
    assert unknown == {200: 1}


def test_message_counts_are_not_bytes():
    calls, _ = nettrace.decode(_pairs((1.0, 1.1, 299, (5, 0, 8), 3)))
    assert calls[0].kind == "recv" and calls[0].nbytes is None


def test_perf_script_rows_parse_and_pair(tmp_path):
    p = tmp_path / "trace.txt.gz"
    with gzip.open(p, "wt") as f:
        f.write("   200/201  100.000100000: raw_syscalls:sys_enter: NR 102 (a, ffd0c000, 0, 0, 0, 0)\n"
                "   200/201  100.000300000: raw_syscalls:sys_exit: NR 102 = 1448\n"
                "   200/202  100.000400000: raw_syscalls:sys_exit: NR 3 = 0\n"          # its enter was before the recording
                "   200/201  100.000500000: raw_syscalls:sys_enter: NR 168 (ffd0, 1, 3e8, 0, 0, 0)\n")  # still inside at the end
    rows = nettrace.load_rows(str(p))
    pairs, unpaired = nettrace.pair(rows)
    assert pairs == [(100.0001, 100.0003, 200, 201, 102, (10, 0xffd0c000, 0, 0, 0, 0), 1448)]
    assert unpaired == {"exit_without_enter": 1, "enter_without_exit": 1}


def test_filter_covers_both_tables():
    ids = {int(x.split("==")[1]) for x in nettrace.filter_expr().split("||")}
    assert {45, 371, 102, 3, 0, 168, 7} <= ids


# ---- nettrace: the network-wait rule ------------------------------------------------

def _thread(*calls):
    """ThreadCalls from (t_enter, t_exit, kind, ret) with names by kind."""
    name = {"recv": "recvfrom", "fread": "read", "fwrite": "write", "poll": "poll", "send": "sendto"}
    return nettrace.ThreadCalls([nettrace.Call(a, b, 200, 201, name[k], 5, r, k, r if k == "recv" and r > 0 else None)
                                 for a, b, k, r in calls])


def test_a_receive_the_thread_slept_in_that_returns_data_is_a_network_wait():
    tc = _thread((0.9995, 1.0102, "recv", 1448))
    assert tc.network_wait(1.000, 1.010, 1.011) == (True, "recv")


def test_a_poll_with_a_ready_descriptor_then_a_receive_is_a_network_wait():
    tc = _thread((0.9995, 1.0101, "poll", 1), (1.0103, 1.0104, "recv", 16384))
    assert tc.network_wait(1.000, 1.010, 1.011) == (True, "poll")


def test_a_poll_that_timed_out_is_not():
    tc = _thread((0.9995, 1.0101, "poll", 0), (1.0103, 1.0104, "recv", 16384))
    assert tc.network_wait(1.000, 1.010, 1.011) == (False, "poll-no-ready")


def test_a_file_read_before_the_receive_is_not():
    tc = _thread((1.0101, 1.0102, "fread", 4096), (1.0103, 1.0104, "recv", 16384))
    assert tc.network_wait(1.000, 1.010, 1.011) == (False, "file-io-first")


def test_a_receive_without_data_is_passed_over():
    tc = _thread((1.0101, 1.0102, "recv", -11), (1.0103, 1.0104, "recv", 700))
    assert tc.network_wait(1.000, 1.010, 1.011) == (True, "after")


def test_a_receive_after_the_following_wake_is_not():
    tc = _thread((1.0200, 1.0201, "recv", 700))
    assert tc.network_wait(1.000, 1.010, 1.011) == (False, "no-receive")


def test_a_receive_entered_at_the_end_of_the_following_wake_belongs_to_the_next_wait():
    # the thread wakes at 1.010, runs until 1.011 and blocks in a receive that returns at 1.020
    tc = _thread((1.0109, 1.0200, "recv", 700))
    assert tc.network_wait(1.000, 1.010, 1.011) == (False, "no-receive")
    assert tc.network_wait(1.011, 1.0199, 1.021) == (True, "recv")


def test_calls_before_the_interval_do_not_count():
    tc = _thread((0.9000, 0.9001, "recv", 700), (0.9500, 0.9501, "fwrite", 10))
    assert tc.network_wait(1.000, 1.010, 1.011) == (False, "no-receive")


# ---- analyze: wakes, intervals, classes -------------------------------------------

def _seg(t_in, run_ms, state, tid=201, pid=200, comm="steamcmd", delay_ms=0.0, cpu=3):
    return Seg(t_in, t_in - delay_ms / 1000, t_in + run_ms / 1000, run_ms, comm, tid, pid, state, cpu)


def test_intervals_run_from_schedule_out_to_wakeup():
    rows = [_seg(1.000, 1.0, "S"), _seg(1.005, 2.0, "D", delay_ms=1.0), _seg(1.010, 1.0, "S")]
    per, iv, merged = analyze.thread_wakes(rows, {201: [0.999, 1.004, 1.010]})
    assert merged == 0 and len(per[201]) == 3
    assert [round(x["us"]) for x in iv[201]] == [3000, 3000]
    assert [x["state"] for x in iv[201]] == ["S", "D"]
    assert iv[201][0]["next_in"] == 1.005 and iv[201][0]["next_end"] == pytest.approx(1.007)


def test_disk_needs_the_block_io_delay_to_account_for_the_uninterruptible_time():
    iv = {201: [{"us": 6000.0, "state": "D"}, {"us": 4000.0, "state": "D"}, {"us": 5000.0, "state": "S"}]}
    ok = analyze.disk_accounting(iv, {201: 200}, {200: {"blkio_ns": 9_800_000}})
    assert ok[200]["accounted"] and ok[200]["coverage"] == 0.98
    no = analyze.disk_accounting(iv, {201: 200}, {200: {"blkio_ns": 5_000_000}})
    assert not no[200]["accounted"]


def test_classes_follow_the_method_order():
    tc = _thread((1.0101, 1.0102, "recv", 100))     # would match any interval ending at 1.010
    iv = {201: [{"t0": 1.000, "t1": 1.010, "us": 10000.0, "state": "D", "next_in": 1.010, "next_end": 1.011},
                {"t0": 1.000, "t1": 1.010, "us": 10000.0, "state": "S", "next_in": 1.010, "next_end": 1.011},
                {"t0": 2.000, "t1": 2.010, "us": 10000.0, "state": "S", "next_in": 2.010, "next_end": 2.011},
                {"t0": 3.000, "t1": 3.001, "us": 1000.0, "state": "R", "next_in": 3.001, "next_end": 3.002}]}
    analyze.classify(iv, {201: 200}, {200: {"accounted": True}}, {201: tc})
    assert [x["class"] for x in iv[201]] == ["disk", "network", "sleep", "runnable"]
    analyze.classify(iv, {201: 200}, {200: {"accounted": False}}, {201: tc})
    assert iv[201][0]["class"] == "network"   # an unaccounted uninterruptible wait still meets the socket rule here
    analyze.classify(iv, {201: 200}, {200: {"accounted": False}}, None)
    assert [x["class"] for x in iv[201]] == ["uninterruptible", "sleep", "sleep", "runnable"]


def test_an_iowait_row_of_the_thread_makes_its_uninterruptible_wait_a_disk_wait():
    # method §9, the dry-run entry: each wait from its own sched_stat_iowait row, not the process's block-I/O total
    iv = {201: [{"t0": 1.000, "t1": 1.010, "us": 10000.0, "state": "D", "next_in": 1.0102, "next_end": 1.011},
                {"t0": 2.000, "t1": 2.010, "us": 10000.0, "state": "D", "next_in": 2.0102, "next_end": 2.011},
                {"t0": 3.000, "t1": 3.010, "us": 10000.0, "state": "S", "next_in": 3.0102, "next_end": 3.011}]}
    rows = {201: [1.0099, 3.0099], 202: [2.0099]}   # another thread's row does not count
    analyze.classify(iv, {201: 200}, {200: {"accounted": True}}, None, rows)
    assert [x["class"] for x in iv[201]] == ["disk", "uninterruptible", "sleep"]


def test_iowait_rows_parse_from_perf_script():
    text = ("  1234.567890: sched:sched_stat_iowait: comm=CJobMgr::m_Work pid=5108 delay=123456 [ns]\n"
            "  1234.600000: sched:sched_process_exit: comm=borg pid=4571 prio=120\n"
            "  1235.000001: sched:sched_stat_iowait: comm=BgIOThr~Pool #1 pid=77 delay=9 [ns]\n")
    rows = analyze.parse_iowait(text.splitlines())
    assert rows == {5108: [1234.56789], 77: [1235.000001]}


def test_the_transfer_rate_is_the_byte_weighted_median_of_the_per_second_payload():
    C = nettrace.Call
    calls = [C(9.5, 9.5, 200, 201, "recvmsg", 5, 0, "recv", None)]                   # no data: not the start
    calls += [C(float(i), float(i), 200, 201, "recvmsg", 4, 100, "recv", 100) for i in range(10)]   # the login trickle
    calls += [C(10.0 + i * 0.5, 10.0 + i * 0.5, 200, 201, "recvmsg", 5, 1_000_000, "recv", 1_000_000) for i in range(7)]
    calls += [C(11.2, 11.2, 200, 201, "read", 6, 4096, "fread", None)]               # a file read is not payload
    r = analyze.transfer_rate(calls, wire_bytes=7_351_050)
    assert r["payload_bytes"] == 7_001_000
    assert r["per_second_mbps"] == [0.0] * 10 + [16.0, 16.0, 16.0, 8.0]
    assert r["per_second_mbps_byte_weighted_median"] == 16.0   # the trickle's seconds carry almost no bytes
    assert r["wire_over_payload"] == 1.05
    assert analyze.transfer_rate(calls[:2]) is None            # one receive with data: no span


def test_bytes_per_wake_run_from_one_network_wait_to_the_next():
    tc = _thread((1.0101, 1.0102, "recv", 1000), (1.0150, 1.0151, "recv", 500), (1.0301, 1.0302, "recv", 64))
    iv = {201: [{"t0": 1.000, "t1": 1.010, "next_in": 1.0100, "class": "network"},
                {"t0": 1.012, "t1": 1.014, "next_in": 1.0145, "class": "sleep"},
                {"t0": 1.020, "t1": 1.030, "next_in": 1.0300, "class": "network"}]}
    got, unknown = analyze.bytes_per_wake(iv, {201: tc})
    assert got == {201: [1500, 64]} and unknown == 0


def test_the_root_is_the_process_taskset_handed_the_command_to():
    rows = [(1.0, 90, "/usr/bin/taskset"), (1.1, 90, "/usr/bin/perf"),                    # a harness perf launch
            (2.0, 100, "/usr/bin/taskset"), (2.1, 100, "/usr/games/steamcmd"),
            (2.2, 100, "/home/runner/.local/share/Steam/steamcmd/steamcmd.sh"), (2.3, 100, "/usr/bin/bash"),
            (3.0, 200, "/home/runner/.local/share/Steam/steamcmd/linux32/steamcmd")]
    assert analyze.launched_root("steamcmd", rows) == 100
    assert analyze.launched_root("borg", rows) is None


# ---- analyze: one synthetic phase end to end ------------------------------------------

TS_HEADER = ("recv_mono_ns\trecv_real_ns\ttype\tid\tversion\tpid\tppid\ttgid\tcomm\texitcode\tflag\tnice\tsched"
             "\tbtime_s\tetime_us\tutime_us\tstime_us\trun_real_ns\trun_virtual_ns"
             "\tcpu_count\tcpu_delay_ns\tblkio_count\tblkio_delay_ns\tswapin_count\tswapin_delay_ns"
             "\tfreepages_count\tfreepages_delay_ns\tthrashing_count\tthrashing_delay_ns"
             "\tnvcsw\tnivcsw\tminflt\tmajflt\tread_bytes\twrite_bytes\tcancelled_write_bytes\tread_char\twrite_char"
             "\thiwater_rss_kb\thiwater_vm_kb")


def _ts_row(kind, id_, pid, tgid, comm, etime_us, cpu_ns, blkio_ns, t=5.0):
    vals = {"recv_mono_ns": int(t * 1e9), "recv_real_ns": 0, "type": kind, "id": id_, "version": 14, "pid": pid, "ppid": 1,
            "tgid": tgid, "comm": comm, "exitcode": 0, "etime_us": etime_us, "run_virtual_ns": cpu_ns,
            "blkio_delay_ns": blkio_ns}
    return "\t".join(str(vals.get(h, 0)) for h in TS_HEADER.split("\t"))


def _gz(path, text):
    with gzip.open(path, "wt") as f:
        f.write(text)


def _timehist_row(t_out, cpu, comm, tid, pid, delay_ms, run_ms, state):
    return f"{t_out:15.6f} [{cpu:04d}]  {comm}[{tid}/{pid}]  0.000  {delay_ms:.3f}  {run_ms:.3f}  {state}\n"


def test_a_traced_steamcmd_phase_end_to_end(tmp_path):
    D, ph = tmp_path, "steam-fresh-shaped"
    # the wrapper (pid 100, /usr/games/steamcmd -> steamcmd.sh) forks the binary (pid 200), which starts thread 201
    th = (_timehist_row(1.0010, 3, "steamcmd", 100, 100, 0.0, 1.0, "S")
          + _timehist_row(1.0110, 3, "steamcmd", 200, 200, 0.0, 1.0, "S")
          + _timehist_row(1.0210, 3, "CHTTPClientThr", 201, 200, 0.0, 1.0, "S")     # wake 1, then waits
          + _timehist_row(1.0310, 3, "CHTTPClientThr", 201, 200, 0.0, 1.0, "S")     # wake 2 (woken 1.030), then waits
          + _timehist_row(1.0410, 3, "CHTTPClientThr", 201, 200, 0.0, 1.0, "D")     # wake 3 (woken 1.040), then disk
          + _timehist_row(1.0510, 3, "CHTTPClientThr", 201, 200, 0.0, 1.0, "S")     # wake 4 (woken 1.050)
          + _timehist_row(1.0600, 3, "Runner.Worker", 900, 900, 0.0, 2.0, "S"))    # outside the tree
    _gz(D / f"perf.{ph}.timehist.txt.gz", th)
    _gz(D / f"perf.{ph}.wakeups.txt.gz",
        "       1.029900 [0001]  swapper[0]  awakened: CHTTPClientThr[201/200]\n"
        "       1.039900 [0001]  swapper[0]  awakened: CHTTPClientThr[201/200]\n"
        "       1.049900 [0001]  swapper[0]  awakened: CHTTPClientThr[201/200]\n")
    _gz(D / f"perf.{ph}.forks.txt.gz",
        "       0.999000: sched:sched_process_exec: filename=/usr/games/steamcmd pid=100 old_pid=100\n"
        "       1.005000: sched:sched_process_fork: comm=steamcmd pid=100 child_comm=steamcmd child_pid=200\n"
        "       1.006000: sched:sched_process_exec: filename=/home/runner/.steam/steamcmd/linux32/steamcmd pid=200 old_pid=200\n"
        "       1.015000: sched:sched_process_fork: comm=steamcmd pid=200 child_comm=steamcmd child_pid=201\n")
    (D / f"taskstats.{ph}.tsv").write_text(
        "# started_mono_ns=0\n" + TS_HEADER + "\n"
        + _ts_row("pid", 201, 201, 200, "CHTTPClientThr", 40_000, 4_000_000, 0) + "\n"
        + _ts_row("pid", 200, 200, 200, "steamcmd", 60_000, 1_000_000, 0) + "\n"
        + _ts_row("tgid", 200, 0, 0, "", 0, 5_000_000, 0) + "\n"
        + _ts_row("pid", 100, 100, 100, "steamcmd.sh", 70_000, 1_000_000, 0) + "\n"
        + "# stopped_mono_ns=9 rows=4 enobufs=0 errors=0\n")
    (D / f"execs.{ph}.tsv").write_text("/usr/games/steamcmd\tscript\n/home/runner/.steam/steamcmd/linux32/steamcmd\tELF32\n")
    # thread 201: socketcall recv spanning the first wait (1448 B), a poll then recv after the second, nothing after the disk wait
    _gz(D / f"trace.{ph}.txt.gz",
        "   200/201       1.021000000: raw_syscalls:sys_enter: NR 102 (a, ffd0, 0, 0, 0, 0)\n"
        "   200/201       1.030100000: raw_syscalls:sys_exit: NR 102 = 1448\n"
        "   200/201       1.031000000: raw_syscalls:sys_enter: NR 168 (ffd0, 1, 3e8, 0, 0, 0)\n"
        "   200/201       1.040100000: raw_syscalls:sys_exit: NR 168 = 1\n"
        "   200/201       1.040200000: raw_syscalls:sys_enter: NR 102 (a, ffd0, 0, 0, 0, 0)\n"
        "   200/201       1.040300000: raw_syscalls:sys_exit: NR 102 = 16384\n")
    edges = {ph: {"start": 0, "end": int(2e9), "cmd_wall_s": 1.5, "rc": 0}}
    r = analyze.analyze_phase(str(D), ph, 3, edges, {f"net.{ph}.rx_bytes": "1000000"})
    assert r["program_pids"] == [200]
    assert r["tree_processes"] == 2 and "Runner.Worker" in r["outside_on_measured_cpu"]
    assert r["network"]["compat_pids"] == [200] and not r["network"]["compat_assumed"]
    t = r["threads"]["CHTTPClientThr#1"]
    assert t["wakes"] == 4 and t["network_us"]["n"] == 2 and t["uninterruptible_us"]["n"] == 1
    assert r["_samples"]["threads"]["CHTTPClientThr#1"]["bytes_per_wake"] == [1448, 16384]
    assert r["network"]["network_rule"]["recv"] == 1 and r["network"]["network_rule"]["poll"] == 1
    assert r["network"]["achieved_mbps_counters"] == pytest.approx(1000000 * 8 / 1.5 / 1e6, abs=0.01)
    p200 = next(p for p in r["processes"] if p["pid"] == 200)
    assert p200["taskstats_cpu_us"] == 5000.0 and p200["perf_cpu_us"] == pytest.approx(5000.0)


# ---- fileset: the change set, the manifest, the set check ----------------------------

def _tree(root, sizes):
    for i, s in enumerate(sizes):
        d = root / f"d{i % 3}"
        d.mkdir(exist_ok=True)
        (d / f"f{i:03d}").write_bytes(bytes((i + k) % 251 for k in range(s)))


def test_the_change_set_is_seeded_and_stays_under_its_targets(tmp_path):
    root = tmp_path / "set"
    root.mkdir()
    _tree(root, [1000 + 997 * i for i in range(200)])
    entries = [(r, (root / r).stat().st_size) for r in fileset.files_of(str(root))]
    a = fileset.plan_change(entries, fileset.dirs_of(str(root)))
    b = fileset.plan_change(entries, fileset.dirs_of(str(root)))
    assert a == b
    assert a["target_changed_bytes"] == round(a["set_bytes"] * 29.9 / 2370)
    assert 0 < a["changed_file_bytes"] <= a["target_changed_bytes"]
    assert a["new_bytes"] == a["target_new_bytes"] == round(a["set_bytes"] * 10.3 / 2370)
    assert all(1 <= c["length"] <= c["size"] and c["offset"] + c["length"] <= c["size"] for c in a["changed"])


def test_change_then_restore_returns_the_manifest(tmp_path):
    root, stash = tmp_path / "set", tmp_path / "stash"
    root.mkdir()
    _tree(root, [5000 + 331 * i for i in range(60)])
    manifest = fileset.scan(str(root), workers=1)
    entries = [(r, s) for r, s, _ in manifest]
    plan = fileset.plan_change(entries, fileset.dirs_of(str(root)))
    fileset.apply_change(str(root), str(stash), plan)
    after = fileset.verify(str(root), manifest)
    assert not after["ok"] and after["differ"] == len(plan["changed"]) and after["extra"] == len(plan["new"])
    fileset.restore_change(str(root), str(stash), plan)
    assert fileset.verify(str(root), manifest)["ok"]


def test_manifest_round_trip_and_set_check(tmp_path):
    root = tmp_path / "set"
    root.mkdir()
    _tree(root, [10, 20, 30])
    p = tmp_path / "m.tsv.gz"
    fileset.write_manifest(fileset.scan(str(root), workers=1), str(p))
    m = fileset.read_manifest(str(p))
    assert [s for _, s, _ in m] == [10, 20, 30]
    chk = fileset.set_check(m + [("big", 31 * 2**20, "x")])
    assert chk["median_file_bytes"] == 25 and chk["share_bytes_over_30e6"] == chk["share_bytes_over_30MiB"] > 0.99


# ---- appinfo: sizes and the branch to stage ----------------------------------------------

APPINFO = '''AppID : 232250, change number : 1/0
"232250"
{
	"common"
	{
		"name"		"Team Fortress 2 Dedicated Server"
	}
	"depots"
	{
		"232251"
		{
			"config" { "oslist" "windows" }
			"manifests" { "public" { "gid" "1" "size" "900" "download" "400" } }
		}
		"232252"
		{
			"manifests" { "public" { "gid" "2" "size" "1000" "download" "500" } }
		}
		"232253"
		{
			"config" { "oslist" "linux" }
			"maxsize" "300"
			"manifests" { "public" "3" }
		}
		"branches"
		{
			"public" { "buildid" "100" "timeupdated" "5" }
			"previous" { "buildid" "90" }
			"older" { "buildid" "80" }
			"beta" { "buildid" "95" "pwdrequired" "1" }
			"prerelease" { "buildid" "120" }
		}
	}
}
'''


def test_appinfo_linux_size_and_the_nearest_older_public_branch():
    s = appinfo.summary(appinfo.app_block(APPINFO, 232250))
    assert s["name"] == "Team Fortress 2 Dedicated Server"
    assert s["size"] == 1300 and s["download"] == 500
    assert appinfo.older_branch(s["branches"]) == "previous"


def test_appinfo_block_is_the_app_not_a_depot_with_its_id(tmp_path):
    same = APPINFO.replace('"232252"', '"232250"')      # the app's own id as a depot id (Team Fortress 2's server)
    s = appinfo.summary(appinfo.app_block(same, 232250))
    assert s["name"] == "Team Fortress 2 Dedicated Server" and s["size"] == 1300


def test_smallest_passes_over_apps_with_depots_of_unknown_size(tmp_path, capsys):
    unknown = APPINFO.replace('"232253"\n\t\t{\n\t\t\t"config" { "oslist" "linux" }\n\t\t\t"maxsize" "300"',
                              '"232253"\n\t\t{\n\t\t\t"config" { "oslist" "linux" }')
    small = APPINFO.replace("232250", "244310").replace('"size" "1000"', '"size" "5000"')
    (tmp_path / "appinfo.232250.txt").write_text(unknown)
    (tmp_path / "appinfo.244310.txt").write_text(small)
    import sys
    argv, sys.argv = sys.argv, ["appinfo.py", "smallest", str(tmp_path / "appinfo.232250.txt"), str(tmp_path / "appinfo.244310.txt")]
    try:
        appinfo.main()
    finally:
        sys.argv = argv
    assert capsys.readouterr().out.strip() == "244310"


def test_appinfo_takes_the_last_printed_block():
    stale = APPINFO.replace('"size" "1000"', '"size" "1"')
    s = appinfo.summary(appinfo.app_block(stale + APPINFO, 232250))
    assert s["size"] == 1300


# ---- pool: the first batch, the checks, the comparisons ----------------------------------

RUN = "borg-first-warm run between voluntary blocks (µs)"


def _one_sample_each(values):
    return _entry("borg-first-warm", {"batch_run_us": {k: [v] for k, v in enumerate(values, 1)}})


def test_first_batch_is_the_smallest_count_that_passes_at_the_probe_spread():
    # mean 100, sd 6: t(k-1) * 6 / sqrt(k) / 100 <= 0.05 first at k = 9 (2.306 * 6 / 3 = 4.61; k = 8: 5.02)
    assert pool.criterion("borg", _one_sample_each([94.0, 100.0, 106.0]))[RUN]["needed"] == 9
    assert pool.criterion("borg", _one_sample_each([100.0, 100.0, 100.0]))[RUN]["needed"] == 5   # five repeats (D18)
    assert pool.criterion("borg", _one_sample_each([100.0]))[RUN]["needed"] is None


def test_first_batch_takes_the_absolute_floor_for_small_medians():
    # mean 10 µs, sd 1: 5 % is 0.5 µs, the floor 1 µs; t(k-1) / sqrt(k) <= 1 first at k = 7 (2.447 / 2.646 = 0.925)
    assert pool.criterion("borg", _one_sample_each([9.0, 10.0, 11.0]))[RUN]["needed"] == 7


def test_first_batch_past_twenty_repeats_takes_students_t_not_the_normal():
    # sd 15 about 100: t(k-1) / sqrt(k) <= 1/3 first at k = 38; the normal's 1.96 would stop at 35
    assert pool.criterion("borg", _one_sample_each([85.0, 100.0, 115.0]))[RUN]["needed"] == 38


def test_the_rule_needs_five_repeats_and_floors_times():
    assert not pool.criterion("borg", _one_sample_each([10.0] * 4))[RUN]["passes"]
    assert pool.criterion("borg", _one_sample_each([10.0] * 5))[RUN]["passes"]
    near = [9.0, 10.0, 11.0, 9.0, 11.0, 10.0, 10.0]   # ±9 % of the mean, within 1 µs
    assert pool.criterion("borg", _one_sample_each(near))[RUN]["passes"]
    assert pool.floor_of("bytes_per_wake") is None      # bytes carry no time floor


def test_the_rule_weighs_each_repeat_by_its_samples():
    # one repeat of a single 200 µs run beside four of 99 runs at 100 µs: the per-repeat means 200, 100, 100, 100, 100
    # read ±46 %, the table the fold-in carries has mean 39 800 / 397 = 100.25 µs and holds within ±0.9 %
    tables = {1: [200.0], **{k: [100.0] * 99 for k in range(2, 6)}}
    c = pool.criterion("borg", _entry("borg-first-warm", {"batch_run_us": tables}))[RUN]
    assert c["mean"] == pytest.approx(39800 / 397, abs=1e-4) and c["half_width"] < 0.01 and c["passes"]


def test_a_pooled_table_carries_each_repeats_mean():
    p = pool.pooled({1: [1.0, 2.0, 9.0], 2: [4.0], 3: []})
    assert p["repeat_mean"] == {1: 4.0, 2: 4.0, 3: None}
    assert p["repeat_p50"] == {1: 2.0, 2: 4.0, 3: None}


def _entry(phase, tables):
    return {"phases": {phase: {"all": {k: pool.pooled(v) for k, v in tables.items()}}}}


def test_the_rule_tests_every_table_on_the_list_by_its_mean():
    # medians identical in every repeat, means apart by the long tail: the rule reads the means (D19)
    steady_p50_wild_mean = {k: [10.0, 10.0, 10.0 + 40.0 * (k % 2)] for k in range(1, 6)}
    flat = {k: [10.0, 10.0, 10.0] for k in range(1, 6)}
    crit = pool.criterion("borg", _entry("borg-first-warm", {"batch_run_us": flat, "batch_block_us": steady_p50_wild_mean}))
    assert set(crit) == {"borg-first-warm run between voluntary blocks (µs)", "borg-first-warm block per run (µs)"}
    assert crit["borg-first-warm run between voluntary blocks (µs)"]["passes"]
    assert not crit["borg-first-warm block per run (µs)"]["passes"]
    assert crit["borg-first-warm run between voluntary blocks (µs)"]["needed"] == 5


def test_the_list_is_each_archetypes_batch_loop_tables():
    # D29: every archetype compiles as cpu-batch's batch loop and carries its two tables
    for app in ("borg", "7z", "steamcmd"):
        assert [k for _p, k, _l in pool.LIST[app]] == ["batch_run_us", "batch_block_us"]
    assert {p for _p in pool.LIST.values() for p, _k, _l in _p} == {"borg-first-warm", "7z-mmt8-warm", "steam-fresh-shaped"}


def test_a_difference_inside_the_precision_is_not_resolved():
    assert pool.compare(100.0, 104.0)["reading"] == "not resolved"
    assert pool.compare(100.0, 106.0)["reading"] == "difference"
    assert pool.compare(None, 1.0)["reading"] is None


def test_a_check_is_read_against_the_interval_of_its_per_repeat_ratios():
    # D36: a D15 check is a difference when the 95 % interval of its per-repeat ratios excludes 1. Ratios 0.97, 0.98,
    # 0.975, 0.97, 0.98: mean 0.975, sd 0.005, interval 0.975 ± 2.776 · 0.005 / sqrt(5) = 0.9688–0.9812 — a 2.5 % shift
    # in every repeat, which the ±5 % reading of a comparison would call not resolved
    steady = {1: 0.97, 2: 0.98, 3: 0.975, 4: 0.97, 5: 0.98}
    c = pool.check(100.0, 97.5, steady)
    assert c["ratio"] == 0.975 and c["reading"] == "difference"
    assert c["per_repeat_mean"] == 0.975 and c["interval"] == [0.9688, 0.9812]
    assert pool.compare(100.0, 97.5)["reading"] == "not resolved"
    # ratios straddling 1 do not resolve, however far the pooled medians' ratio sits from it
    wide = {1: 0.9, 2: 1.1, 3: 0.95, 4: 1.05, 5: 1.0}
    assert pool.check(100.0, 110.0, wide)["reading"] == "not resolved"
    assert pool.check(None, 1.0, steady)["reading"] is None


def test_a_stopped_job_keeps_its_gate(tmp_path):
    # the machine gate and the network gate (D27) each stop a job before it measures; the pooled record names which
    for run, name, gate, model in (("11", "meas-background-steamcmd-r1-full", "wrong-machine", "AMD EPYC 9V74 80-Core Processor"),
                                   ("12", "meas-background-steamcmd-r2-full", "no-vf", "AMD EPYC 7763 64-Core Processor")):
        d = tmp_path / run / name
        d.mkdir(parents=True)
        (d / "report.json").write_text(json.dumps({"gate": gate, "machine.model": model}))
    runs, gated, other = pool.find_runs(str(tmp_path), "EPYC 7763")
    assert runs == {} and other == []
    assert gated == [
        {"app": "steamcmd", "repeat": 1, "gate": "wrong-machine", "cpu_model": "AMD EPYC 9V74 80-Core Processor",
         "path": "11/meas-background-steamcmd-r1-full"},
        {"app": "steamcmd", "repeat": 2, "gate": "no-vf", "cpu_model": "AMD EPYC 7763 64-Core Processor",
         "path": "12/meas-background-steamcmd-r2-full"}]


def test_the_page_counts_the_machine_gate_and_the_network_gate_apart():
    out = {"tag": None, "machine": "EPYC 7763", "other_machine": [], "runs": {},
           "gated_out": [{"gate": "wrong-machine"}, {"gate": "wrong-machine"}, {"gate": "no-vf"}]}
    assert "; stopped by the machine gate 2, by the network gate 1; other-model repeats 0." in pool.render(out)
    out["gated_out"] = out["gated_out"][:2]
    assert "; stopped by the machine gate 2; other-model repeats 0." in pool.render(out)
