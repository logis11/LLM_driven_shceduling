"""9.10's span probes (changelog D143, D144): the readings and the workflow's plan."""
import json
import os
import pathlib
import subprocess
import sys
import textwrap

import pytest
import yaml

from meas.campaign import span_probe as sp

REPO = pathlib.Path(__file__).resolve().parents[3]


def test_a_flat_profile_holds_at_every_placement():
    r = sp.level_reading([2.0] * 30, [100.0] * 30, 10.0, 60.0, 300.0)
    assert r["holds"] and r["cpu_ms_per_s"]["placement"] == 0 and r["wakes_per_s"]["worst"] == 0


def test_a_first_window_above_the_span_level_does_not_hold():
    # the phase's first 60 s at 3 ms/s, the rest of a 300 s span at 2: level 2.2, placement +36 %
    cpu = [3.0] * 6 + [2.0] * 24
    r = sp.level_reading(cpu, [100.0] * 30, 10.0, 60.0, 300.0)
    assert r["cpu_ms_per_s"]["level"] == pytest.approx(2.2)
    assert r["cpu_ms_per_s"]["placement"] == pytest.approx(3 / 2.2 - 1, abs=1e-4)
    assert not r["cpu_ms_per_s"]["holds"] and r["wakes_per_s"]["holds"] and not r["holds"]


def test_the_worst_placement_is_found_inside_the_span_only():
    # a burst at 200–210 s inside the span; another past it, at 400 s, outside
    wakes = [100.0] * 50
    wakes[20], wakes[40] = 400.0, 9000.0
    r = sp.level_reading([2.0] * 50, wakes, 10.0, 60.0, 300.0)
    assert r["wakes_per_s"]["worst_at_s"] in {150.0, 160.0, 170.0, 180.0, 190.0, 200.0}
    assert r["wakes_per_s"]["placement"] < 0 < r["wakes_per_s"]["worst"]


def test_a_probe_shorter_than_its_span_is_refused():
    with pytest.raises(ValueError, match="short of the 400 s span"):
        sp.level_reading([1.0] * 30, [1.0] * 30, 10.0, 60.0, 400.0)


def test_rows_are_sliced_by_their_schedule_in():
    cpu, wakes = sp.slices_of_rows([(100.5, 2.0), (101.0, 3.0), (115.0, 4.0), (131.0, 9.0)], 100.0, 30.0, 10.0)
    assert cpu == [0.5, 0.4, 0.0] and wakes == [0.2, 0.1, 0.0]


def test_paired_windows_equal_to_their_repeats_are_not_resolved():
    camp = {k: 50.0 + k for k in range(1, 22)}
    probe = {k: v * (1.0 + (0.01 if k % 2 else -0.01)) for k, v in camp.items()}
    r = sp.paired_reading(probe, camp)
    assert r["windows"] == list(range(1, 22)) and r["reading"] == "not resolved"
    assert r["interval"][0] <= 1 <= r["interval"][1] and r["trend"]["reading"] == "not resolved"


def test_a_cost_growing_with_the_session_is_a_difference_and_a_trend():
    camp = {k: 50.0 for k in range(1, 22)}
    probe = {k: 50.0 * (1 + 0.02 * (k - 1)) for k in camp}
    r = sp.paired_reading(probe, camp)
    assert r["reading"] == "difference" and r["per_window_mean"] == pytest.approx(1.2)
    assert r["trend"]["reading"] == "difference" and r["trend"]["per_window"] == pytest.approx(0.02)


def test_a_window_the_campaign_does_not_hold_is_left_out():
    camp = {k: 50.0 for k in range(1, 6)}
    probe = {k: 50.0 for k in range(1, 8)}
    probe[3] = None
    assert sp.paired_reading(probe, camp)["windows"] == [1, 2, 4, 5]


def test_the_campaign_means_follow_the_pooled_repeats():
    pool = {"runs": {"code": {"phases": {"driven": {"repeats": [1, 2, 4],
            "per_input": {"window": {"run_ms_minus_idle": {"repeat_mean": [10.0, 11.0, 13.0]}}}}}}}}
    assert sp.campaign_means(pool, "code") == {1: 10.0, 2: 11.0, 4: 13.0}


def test_a_window_is_viewed_as_the_driven_phase_beside_the_idle_phase(tmp_path):
    run = tmp_path / "run"
    run.mkdir()
    for f in ("report.json", "perf.idle.timehist.txt.gz", "snap.idle.before.json", "perf.driven-w02.timehist.txt.gz",
              "perf.driven-w02.wakeups.txt.gz", "snap.driven-w02.after.json", "replay.driven-w02.jsonl",
              "perf.driven-w10.timehist.txt.gz", "replay.driven-w10.jsonl"):
        (run / f).write_text(f)
    assert sp.window_names(run) == ["driven-w02", "driven-w10"]
    v = pathlib.Path(sp.view(str(run), "driven-w02", str(tmp_path / "v")))
    assert sorted(os.listdir(v)) == ["perf.driven.timehist.txt.gz", "perf.driven.wakeups.txt.gz",
                                     "perf.idle.timehist.txt.gz", "replay.jsonl", "report.json",
                                     "snap.driven.after.json", "snap.idle.before.json"]
    assert (v / "replay.jsonl").read_text() == "replay.driven-w02.jsonl"


def plan(tmp_path, trigger):
    """The long-probe workflow's plan step run on a trigger: {output: value}."""
    wf = yaml.safe_load((REPO / ".github/workflows/meas-long-probe.yml").read_text())
    script = next(s["run"] for s in wf["jobs"]["plan"]["steps"] if s.get("id") == "plan")
    body = textwrap.dedent(script.split("<<'PY'\n", 1)[1].rsplit("PY", 1)[0])
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github/campaign-long-probe.json").write_text(json.dumps(trigger))
    out = subprocess.run([sys.executable, "-c", body], cwd=tmp_path, capture_output=True, text=True, check=True).stdout
    return dict(line.split("=", 1) for line in out.splitlines())


def test_the_plan_runs_a_driven_index_in_probe_driven_mode(tmp_path):
    out = plan(tmp_path, {"mode": "probe", "cpu_model": "EPYC 7763", "apps": ["code", "kdenlive", "soffice"],
                          "repeats": {"code": [11], "kdenlive": [10, 11], "soffice": [10]},
                          "phase_s": {"kdenlive": 3000, "soffice": 1500},
                          "driven": {"code": [11], "kdenlive": [11]}, "windows": {"code": 21, "kdenlive": 8}})
    inc = {(j["app"], j["repeat"]): j for j in json.loads(out["matrix"])["include"]}
    assert inc[("code", 11)] == {"app": "code", "repeat": 11, "run_mode": "probe-driven", "phase_s": 0,
                                 "windows": 21, "window_s": 600}
    assert inc[("kdenlive", 10)]["run_mode"] == "probe" and inc[("kdenlive", 10)]["phase_s"] == 3000
    assert inc[("kdenlive", 11)]["windows"] == 8 and inc[("soffice", 10)]["phase_s"] == 1500
    assert out["mode"] == "probe" and out["count"] == "4"


def test_the_plan_keeps_9_5s_trigger_form(tmp_path):
    out = plan(tmp_path, {"mode": "probe", "apps": ["webrtc"], "repeats": {"webrtc": [1]}, "phase_s": {"webrtc": 2000}})
    assert json.loads(out["matrix"])["include"] == [{"app": "webrtc", "repeat": 1, "run_mode": "probe",
                                                     "phase_s": 2000, "windows": 0, "window_s": 0}]
