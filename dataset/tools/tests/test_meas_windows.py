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
