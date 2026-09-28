"""A desktop long-phase probe read in time windows (9.8 D35)."""
import pytest

from meas.desktop import probe_windows as pw


def test_the_probe_reads_short_windows_and_windows_of_the_carried_phase_s_length():
    rows = [("a", 0.0, 1.0), ("a", 150.0, 1.0), ("a", 650.0, 1.0), ("b", 1300.0, 2.0)]
    r = pw.read_probe(rows, 0.0, 1800.0, 600.0)
    assert r["short"]["windows"] == 18 and r["carried"]["windows"] == 3
    assert r["carried"]["components"]["a"]["wakes_per_s"] == pytest.approx([2 / 600, 1 / 600, 0.0])
    assert r["carried"]["components"]["b"]["run_mean_ms"] == [None, None, 2.0]


def test_the_page_carries_both_readings():
    r = pw.read_probe([("a", 0.0, 1.0), ("a", 650.0, 3.0)], 0.0, 1200.0, 600.0)
    rec = {"archetype": "chat-client", "app": "element", "version": "1.12.28", "span_s": 1200.0, "carried_s": 600.0, **r}
    page = pw.render(rec)
    assert "# chat-client (`element`): the long-phase probe in time windows" in page
    assert "Element 1.12.28, one job, 1200 s" in page
    assert "In windows of the carried phase's length, 600 s" in page
