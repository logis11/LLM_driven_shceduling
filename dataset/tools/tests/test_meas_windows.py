"""The carried phases read in time windows (meas/windows.py, the 2026-09-28 review of 9.5–9.9)."""
import pytest

from meas import windows


def test_a_row_falls_in_the_window_its_schedule_in_falls_in_and_only_whole_windows_are_read():
    rows = [("a", 10.0, 1.0), ("a", 109.0, 2.0), ("b", 150.0, 4.0), ("a", 250.0, 8.0)]
    n, w = windows.read(rows, 10.0, 250.0, 100.0)   # the phase [10, 260): windows [10, 110), [110, 210); 210–260 not whole
    assert n == 2
    assert w[0] == {"a": [2, 3.0], "ALL": [2, 3.0]}
    assert w[1] == {"b": [1, 4.0], "ALL": [1, 4.0]}


def test_the_windows_pool_over_the_repeats_time_in_them():
    r1 = windows.read([("a", 0.0, 1.0), ("a", 150.0, 3.0)], 0.0, 200.0, 100.0)
    r2 = windows.read([("a", 50.0, 1.0), ("a", 60.0, 1.0)], 0.0, 300.0, 100.0)
    e = windows.pool([r1, r2], 100.0)
    assert e["windows"] == 2 and e["repeats"] == 2          # the shorter repeat bounds the windows read
    a = e["components"]["a"]
    assert a["wakes_per_s"] == pytest.approx([3 / 200, 1 / 200])
    assert a["run_mean_ms"] == pytest.approx([1.0, 3.0])
    assert a["cpu_ms_per_s"] == pytest.approx([3 / 200, 3 / 200])


def test_a_component_s_cpu_above_its_median_window_is_read_as_a_share_of_the_phase():
    e = {"components": {"ALL": {"cpu_ms_per_s": [4.0, 1.0, 1.0, 1.0, 1.0]},
                        "a": {"cpu_ms_per_s": [3.0, 0.0, 0.0, 0.0, 0.0]},
                        "b": {"cpu_ms_per_s": [1.0, 1.0, 1.0, 1.0, 1.0]}}}
    s = windows.shares(e)
    assert s["a"]["share_of_cpu"] == pytest.approx(3 / 8) and s["a"]["above_median_window"] == pytest.approx(3 / 8)
    assert s["b"]["above_median_window"] == 0.0 and s["ALL"]["share_of_cpu"] == 1.0


def test_a_short_phase_reads_short_windows():
    assert windows.window_of(120.0) == windows.SHORT_WIN_S and windows.window_of(600.0) == windows.WIN_S


def test_the_page_carries_each_component_s_windows():
    r = windows.read([("a", 0.0, 1.0), ("a", 150.0, 3.0)], 0.0, 200.0, 100.0)
    e = windows._entry("office-writer", "soffice", "idle", [r], 100.0)
    page = windows.render({"family": "campaign", "archetypes": {"office-writer": e}})
    assert "## office-writer (`soffice`, idle)" in page and "1 repeats, 2 whole windows of 100 s" in page
    assert "| `a` | 0.01 | 1.00 · 1.00 | 1.000 · 3.000 | 100.0 % | 25.0 % |" in page


def test_an_operation_s_rows_fall_in_the_window_its_trigger_falls_in_read_over_the_operations_time():
    ops = [(10.0, 12.0), (105.0, 111.0), (150.0, 151.0), (215.0, 216.0)]    # the last triggered past the whole windows
    rows = [("a", 10.5, 1.0), ("a", 109.0, 2.0), ("b", 110.5, 4.0), ("a", 150.2, 8.0), ("a", 215.5, 1.0)]
    by_time, by_op = windows.read_ops(rows, ops, 10.0, 250.0, 100.0)
    n, w, secs = by_time
    assert n == 2
    assert w[0] == {"a": [2, 3.0], "b": [1, 4.0], "ALL": [3, 7.0]}      # the second operation ends past 110 s: still window 0
    assert w[1] == {"a": [1, 8.0], "ALL": [1, 8.0]}
    assert secs == {0: pytest.approx(8.0), 1: pytest.approx(1.0)}


def test_the_operations_read_one_by_one_each_operation_a_window_of_its_own():
    ops = [(0.0, 2.0), (10.0, 11.0), (20.0, 24.0)]
    rows = [("a", 0.5, 1.0), ("a", 1.5, 1.0), ("a", 22.0, 3.0)]
    _, (n, w, secs) = windows.read_ops(rows, ops, 0.0, 30.0, 100.0)
    assert n == 3
    assert w[0] == {"a": [2, 2.0], "ALL": [2, 2.0]} and 1 not in w and w[2] == {"a": [1, 3.0], "ALL": [1, 3.0]}
    assert secs == {0: 2.0, 1: 1.0, 2: 4.0}


def test_an_operation_window_pools_over_the_operations_time_in_it():
    r1 = (2, {0: {"a": [4, 4.0]}, 1: {"a": [1, 1.0]}}, {0: 2.0, 1: 1.0})
    r2 = (2, {0: {"a": [2, 6.0]}}, {0: 2.0})
    e = windows.pool([r1, r2], 100.0)
    a = e["components"]["a"]
    assert a["wakes_per_s"] == pytest.approx([6 / 4, 1 / 1])
    assert a["run_mean_ms"] == pytest.approx([10 / 6, 1.0])
    assert a["cpu_ms_per_s"] == pytest.approx([10 / 4, 1.0])
    assert e["time_s"] == pytest.approx([4.0, 1.0])


def test_the_operations_join_in_blocks_of_consecutive_operations():
    r = (5, {k: {"a": [k + 1, 1.0 * (k + 1)]} for k in range(5)}, {k: 1.0 for k in range(5)})
    e = windows.pool([r], None)
    b = windows.blocks(e, 2)                                  # operations 1–2, 3–4, 5
    assert b["windows"] == 3 and b["time_s"] == pytest.approx([2.0, 2.0, 1.0])
    assert b["components"]["a"]["wakes_per_s"] == pytest.approx([3 / 2, 7 / 2, 5.0])
    assert b["components"]["a"]["run_mean_ms"] == pytest.approx([1.0, 1.0, 1.0])


def test_every_9_5_operation_is_read():
    import yaml
    from meas import control_report as cr
    lib = yaml.safe_load(open(cr.REPO + "/dataset/archetypes.yaml"))["archetypes"]
    with_ops = {app for app, arch in cr.ARCH_95.items() if lib[arch]["params"].get("operations")}
    assert set(windows.OPS_95) == with_ops


def test_the_page_carries_an_operation_phase_in_time_windows_and_by_operation():
    ops = [(0.0, 1.0), (100.0, 101.0)]
    by_time, by_op = windows.read_ops([("a", 0.5, 1.0), ("a", 0.6, 1.0), ("a", 100.5, 3.0)], ops, 0.0, 200.0, 100.0)
    e = windows._entry("mail-client", "thunderbird-send", "op", [by_time], 100.0)
    e["operation"] = "send"
    e["by_operation"] = windows.pool([by_op], None)
    page = windows.render({"family": "campaign", "archetypes": {"mail-client/send": e}})
    assert "## mail-client (`thunderbird-send`, the `send` operation)" in page
    assert "1 repeats, 2 whole windows of 100 s, each holding the operations triggered in it" in page
    assert "| `a` | 1.5 | 1.33 · 0.67 | 1.000 · 3.000 | 100.0 % | 10.0 % |" in page
    assert "By operation, in blocks of 1 (2 operations a repeat)" in page


def test_the_page_names_the_block_that_holds_the_remaining_operations():
    ops = [(float(k), k + 0.5) for k in range(3)]
    by_time, by_op = windows.read_ops([("a", 0.2, 1.0)], ops, 0.0, 200.0, 100.0)
    e = windows._entry("web-browser", "chrome", "op", [by_time], 100.0)
    e.update({"operation": "page-load", "by_operation": windows.pool([by_op], None)})
    old, windows.BLOCKS = windows.BLOCKS, 2
    try:
        page = windows.render({"family": "campaign", "archetypes": {"web-browser/page-load": e}})
    finally:
        windows.BLOCKS = old
    assert "By operation, in blocks of 2 (3 operations a repeat, the last block the remaining 1)" in page
