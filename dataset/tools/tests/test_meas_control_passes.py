"""The untraced control's operation passes read by operation (9.5 D87)."""
import pytest

from meas import windows
from meas.campaign import control_passes as cpass


def test_a_job_s_traced_pass_is_the_one_its_order_traces_first_or_second():
    assert cpass.pass_of("traced untraced") == "first" and cpass.pass_of("untraced traced") == "second"


def test_the_threads_read_by_name_are_the_ones_the_stated_lines_name():
    from meas import control_report as cr
    for app, names in cpass.STATED.items():
        for name in names:
            assert f"`{name}`" in cr.NOTES_STATED[cr.ARCH_95[app]]


def test_a_job_reads_its_first_operations_one_by_one_and_the_rest_as_a_rate():
    ops = [(0.0, 1.0), (10.0, 11.0), (20.0, 21.0), (30.0, 32.0), (40.0, 42.0)]
    rows = [("x", 0.5, 1.0)] * 5 + [("x", 10.5, 1.0), ("x", 30.5, 1.0), ("x", 31.0, 1.0), ("x", 40.1, 1.0)]
    _, by_op = windows.read_ops(rows, ops, 0.0, 50.0, 100.0)
    head, rest = cpass.first_and_rest(by_op, "x", 3)
    assert head == [5, 1, 0] and rest == pytest.approx(3 / 4)


def test_the_page_carries_each_pass_and_each_job_s_first_operations():
    ops = [(0.0, 1.0), (100.0, 101.0), (150.0, 151.0), (160.0, 161.0)]
    t, o = windows.read_ops([("x", 0.5, 1.0), ("x", 100.5, 2.0)], ops, 0.0, 200.0, 100.0)
    ent = windows.pool([t], 100.0)
    ent["by_operation"] = windows.pool([o], None)
    ent["jobs"] = {"1": {"x": {"first": [1, 1, 0], "rest_wakes_per_s": 0.0}}}
    rec = {"archetypes": {"web-browser": {"archetype": "web-browser", "app": "chrome", "stated": ["x"], "operation": "page-load",
                                          "passes": {"first": ent}}}}
    page = cpass.render(rec)
    assert "## web-browser (`chrome`, the `page-load` operation's two passes)" in page
    assert "### The first pass traced (job 1)" in page
    assert "| 1 | 1 · 1 · 0 | 0.0 |" in page
