"""The compiled library reproduces what was measured: a measured table keeps its ten quantiles and its mean (each
interval between two quantiles carries the measured mean of the samples it holds), a component's gaps are taken
over its merged wake times and wrap around the span they were observed over, so they sum to it, and every measured
archetype compiles at the wake rate it carries."""

import importlib
import json
import sys

import pytest
import yaml

from meas import distribution
from meas.campaign import analyze as campaign
from wlc import Timeline, compile_timeline, sampling
from wlc.compiler import _component_events, _load_stream

MASSES = [0.01, 0.04, 0.05, 0.15, 0.25, 0.25, 0.15, 0.05, 0.04, 0.009, 0.001]


def _pool():
    saved = sys.modules.pop("analyze", None)
    try:
        return importlib.import_module("meas.campaign.pool")
    finally:
        if saved is not None:
            sys.modules["analyze"] = saved


# ---- the table: ten quantiles, the extremes, and each interval's mean ----

def test_a_table_keeps_the_linear_quantiles_the_campaigns_publish():
    t = distribution.quantile_table(list(range(1, 101)))
    assert t["p"] == pytest.approx([1.99, 5.95, 10.9, 25.75, 50.5, 75.25, 90.1, 95.05, 99.01, 99.901])
    assert (t["min"], t["max"]) == (1, 100)


def test_each_interval_carries_the_mean_of_the_samples_it_holds():
    # the samples each interval holds: 1; 2–5; 6–10; …; 96–99; then sample 100 for (p99, p99.9], above that interval's
    # top knot 99.901, so held at it — the 0.0009 it gives up spread over the others, a thousandth at most each
    t = distribution.quantile_table(list(range(1, 101)))
    assert t["means"] == pytest.approx([1, 3.5, 8, 18, 38, 63, 83, 93, 97.5, 99.901, 100], abs=0.002)


def test_a_lone_extreme_value_keeps_its_whole_weight_in_the_mean():
    t = distribution.quantile_table([1.0] * 999 + [1001.0])
    assert sum(m * x for m, x in zip(MASSES, t["means"])) == pytest.approx(2.0)


T = {"dist": "quantiles", "p": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], "min": 0, "max": 1000,
     "means": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 800], "sampling": "per-iteration", "source": "meas-ci:interactive:3"}
T_MEAN = 50.705   # sum of MASSES x means, by hand


def test_a_table_states_the_mean_of_its_interval_means():
    assert sampling.mean_us(T) == pytest.approx(T_MEAN)


def test_draws_from_a_table_average_to_its_mean():
    n = 200_000
    draws = [sampling._quantile_sample(T, (i + 0.5) / n) for i in range(n)]
    assert sum(draws) / n == pytest.approx(T_MEAN, rel=0.005)


def test_a_draw_at_a_tabulated_probability_is_that_quantile():
    for u, q in zip(sampling.QUANTILE_PROBS, T["p"]):
        assert sampling._quantile_sample(T, u) == q


def test_a_draw_stays_between_its_intervals_quantiles():
    edges = [0.0, *sampling.QUANTILE_PROBS, 1.0]
    bounds = [T["min"], *T["p"], T["max"]]
    for i in range(11):
        for k in range(1, 50):
            u = edges[i] + (edges[i + 1] - edges[i]) * k / 50
            assert bounds[i] <= sampling._quantile_sample(T, u) <= bounds[i + 1]


# ---- the gaps: merged wake times, wrapped around the span ----

def test_gaps_wrap_around_so_they_sum_to_the_span():
    assert distribution.circular_gaps([([1.0, 3.0, 6.0], 0.0, 10.0)]) == pytest.approx([2.0, 3.0, 5.0])


def test_one_wake_is_one_gap_as_long_as_the_span():
    assert distribution.circular_gaps([([4.0], 0.0, 10.0)]) == pytest.approx([10.0])


def test_operation_windows_join_end_to_end_so_the_pause_between_them_is_no_gap():
    segments = [([10.5, 11.0], 10.0, 12.0), ([21.0, 24.0], 20.0, 25.0)]
    assert distribution.circular_gaps(segments) == pytest.approx([0.5, 2.0, 3.0, 1.5])


def test_a_segment_without_a_wake_still_adds_its_span():
    # two renderers of one repeat, the thread waking in one of them: the rate is the mean over both
    assert distribution.circular_gaps([([1.0], 0.0, 10.0), ([], 0.0, 10.0)]) == pytest.approx([20.0])


def _rows(times_by_tid, comm="worker", pid=100):
    return [campaign.Row(t, t, t + 0.0001, 0.1, comm, tid, pid) for tid, ts in times_by_tid.items() for t in ts]


def test_a_components_gaps_are_taken_over_all_its_threads():
    comms = _pool().phase_comms("app", _rows({1: [1.0, 5.0], 2: [3.0]}), {}, [(0.0, 10.0)])
    c = comms["worker"]
    assert (c["wakes"], c["threads"]) == (3, 2)
    assert sorted(c["gaps"]) == pytest.approx([2000.0, 2000.0, 6000.0])


def test_an_operations_gaps_leave_out_the_pause_between_operations():
    rows = _rows({1: [10.5, 21.0], 2: [11.0, 24.0]})
    c = _pool().phase_comms("app", rows, {}, [(10.0, 12.0), (20.0, 25.0)])["worker"]
    assert sorted(c["gaps"]) == pytest.approx([500.0, 1500.0, 2000.0, 3000.0])


def test_the_residual_wraps_around_its_repeats_span():
    from array import array
    pool = _pool()

    def comm(times):
        return {"wakes": {1: len(times)}, "threads": {1: 1}, "gaps": {1: array("d", [1.0] * (len(times) - 1))},
                "runs": {1: array("d", [0.1] * len(times))}, "t_in": {1: array("d", times)}}
    comms = {"main": comm([0.5 + i * 0.01 for i in range(900)]), "a": comm([1.0, 4.0]), "b": comm([2.0])}
    chosen, residual, _ = pool.select_components(comms, {1: 10.0}, [1], segments={1: [(0.0, 10.0)]})
    assert chosen == ["main"]
    assert residual["gap_ms"]["repeat_mean"] == [pytest.approx(10.0 / 3 * 1000)]


def test_a_repeats_wake_rate_is_not_rounded_away():
    c = {"wakes": {1: 5}}
    assert _pool().per_repeat_rates(c, [1], {1: 120.0}) == [pytest.approx(5 / 120)]


def test_a_renderer_threads_rate_is_the_mean_over_every_renderer_measured():
    from meas.desktop import analyze as desktop
    rows = _rows({11: [1.0], 12: [3.0]}, comm="chrome", pid=1) + _rows({21: [2.0, 4.0]}, comm="HangWatcher", pid=2)
    out, samples = desktop.renderer_components(rows, 10.0, 0.0)
    assert out["chrome"]["wakes_per_s"] == pytest.approx(0.1)          # 0.2 and 0 over two renderers
    assert sorted(samples["chrome"]["gaps"]) == pytest.approx([2000.0, 18000.0])


def test_a_session_components_gaps_are_merged_over_its_threads():
    from meas.session import analyze as session
    rows = _rows({1: [1.0, 5.0], 2: [3.0]}, comm="gmain", pid=7)
    _, samples = session.components(rows, {"shell": {7}}, 10.0, 0.0)
    assert sorted(samples["shell/gmain"]["gaps"]) == pytest.approx([2000.0, 2000.0, 6000.0])


# ---- the compiler: what the measurement replayed, and the heavy event ----

def test_a_keys_only_stimulus_replays_only_the_keys():
    kinds = [json.loads(line)["kind"] for line in open(_stream_path("swell-word-c1")) if line.strip()]
    assert len(_load_stream("swell-word-c1", ("key",))) == kinds.count("key")
    assert len(_load_stream("swell-word-c1")) == len(kinds)


def _stream_path(name):
    import pathlib
    return pathlib.Path(__file__).resolve().parents[2] / "stimulus" / f"{name}.jsonl"


def test_a_heavy_event_is_compiled_at_its_rate(tmp_path, repo_root):
    from wlc import Library
    data = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    run = {"dist": "quantiles", "p": [123457] * 10, "min": 123457, "max": 123457, "means": [123457] * 11,
           "sampling": "per-iteration", "source": "meas-ci:interactive:2026-09-20"}
    data["archetypes"]["web-browser"]["params"]["heavy_events"] = [
        {"comm": "MemoryInfra", "run_floor_ms": 30, "count": 8, "span_s": 200.0, "rate_per_s": 0.04, "run": run}]
    lib_path = tmp_path / "archetypes.yaml"
    lib_path.write_text(yaml.safe_dump(data))
    lib = Library(lib_path)
    tl = {"meta": {"id": "x-heavy", "seed": 9, "demand": "calibration"},
          "segments": [{"from": "0s", "to": "5000s", "mode": "office", "attributes": {"background_wanted": True}}],
          "tasks": [{"id": "b", "name": "chrome", "archetype": "web-browser", "arrive": "0s", "depart": "5000s"}],
          "focus": []}
    path = tmp_path / "x-heavy.timeline.yaml"
    path.write_text(yaml.safe_dump(tl))
    canonical, _ = compile_timeline(Timeline(path, lib), lib, "single", rel_path="fx")
    program = next(e for e in canonical["events"] if e["op"] == "arrive")["program"]
    heavy = sum(1 for s in program if s["op"] == "RUN" and s["us"] == 123457)
    assert 150 <= heavy <= 250          # 0.04 /s over 5000 s: 200 expected


# ---- the library: every measured archetype compiles at what it carries ----

def _library(repo_root):
    return yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())["archetypes"]


def _tables(node, where=""):
    if isinstance(node, dict):
        if node.get("dist") == "quantiles":
            yield where, node
        for k, v in node.items():
            yield from _tables(v, f"{where}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _tables(v, f"{where}[{i}]")


def _component_sets(lib):
    for aid, a in lib.items():
        p = a.get("params") or {}
        for key in ("components", "focus_components"):
            if p.get(key):
                yield aid, key, p[key]
        for oname, op in (p.get("operations") or {}).items():
            yield aid, f"operations.{oname}", op["components"]


def test_every_measured_table_carries_its_extremes_and_interval_means(repo_root):
    bare = [f"{aid}{where}" for aid, a in _library(repo_root).items() for where, t in _tables(a.get("params"))
            if not ({"min", "max", "means"} <= set(t) and len(t["means"]) == 11)]
    assert not bare


def test_every_component_compiles_at_its_measured_wake_rate(repo_root):
    off = []
    for aid, where, comps in _component_sets(_library(repo_root)):
        for c in comps:
            implied = 1e6 / sampling.mean_us(c["gap"])
            if abs(implied / c["wakes_per_s"] - 1) > 0.02:
                off.append(f"{aid} {where} {c['comm']}: {implied:.4g} /s against {c['wakes_per_s']:.4g}")
    assert not off, "\n".join(off)


def _second_moment(table, n=20_000):
    return sum(sampling._quantile_sample(table, (i + 0.5) / n) ** 2 for i in range(n)) / n


def test_every_component_set_compiles_at_its_measured_rate_and_cpu(repo_root):
    # the compile path over a finite span: the wake rate within 5 %, the CPU share within four standard errors of the
    # run draws it sums (a send's CPU is 87 % `thunderbird-bin` runs of up to 1.2 s, so 50 000 events are noisy there)
    off = []
    for aid, where, comps in _component_sets(_library(repo_root)):
        rate = sum(c["wakes_per_s"] for c in comps)
        cpu = sum(c["wakes_per_s"] * sampling.mean_us(c["run"]) / 1e6 for c in comps)
        span = int(50_000 / rate * 1e6)
        se = sum(c["wakes_per_s"] * span / 1e6 * _second_moment(c["run"]) for c in comps) ** 0.5 / span
        events = _component_events(comps, 11, "fidelity", 0, span, "fidelity")
        got_rate, got_cpu = len(events) / (span / 1e6), sum(e[1] for e in events) / span
        if abs(got_rate / rate - 1) > 0.05 or abs(got_cpu - cpu) > 4 * se + 0.01 * cpu:
            off.append(f"{aid} {where}: {got_rate:.4g} /s, CPU {got_cpu:.4g} against {rate:.4g} /s, "
                       f"CPU {cpu:.4g} ± {4 * se:.2g}")
    assert not off, "\n".join(off)



def test_every_periodic_archetype_carries_its_measured_cpu(repo_root):
    # 9.5 D75: a periodic job's run is its cycle's whole-tree CPU, so the run table's mean over the period is the play
    # phase's CPU share, inside the range its repeats measured
    periodic = 0
    for aid, a in _library(repo_root).items():
        p = a.get("params") or {}
        if "cycle_run" not in p:
            continue
        periodic += 1
        share = sampling.mean_us(p["cycle_run"]) / p["period"]["value_us"]
        stat = next(s for s in a["validation_stats"]["stats"] if s.startswith("play cpu-share"))
        lo, hi = (float(x) for x in stat.split()[-1].split("\u2013"))
        assert lo <= share <= hi, f"{aid}: {share:.5f} outside {lo}–{hi}"
    assert periodic == 3   # audio-player, video-player, video-call


def test_the_linter_checks_a_tables_extremes_means_and_the_replayed_kinds(tmp_path, repo_root):
    from wlc.linter import lint_repo
    lib = yaml.safe_load((repo_root / "dataset" / "archetypes.yaml").read_text())
    params = lib["archetypes"]["office-writer"]["params"]
    gap, run = params["components"][0]["gap"], params["components"][0]["run"]
    gap.update({"min": 0, "max": gap["p"][-1], "means": [1.0] * 10})                        # ten means for eleven intervals
    run.update({"min": run["p"][0] + 5, "max": run["p"][-1], "means": [run["p"][0]] * 11})   # a minimum above p1
    params["stimulus"]["kinds"] = ["key", "tap"]
    path = tmp_path / "archetypes.yaml"
    path.write_text(yaml.safe_dump(lib))
    joined = "\n".join(lint_repo(path, repo_root / "dataset" / "sources.yaml", repo_root / "docs" / "references.md"))
    assert "eleven interval means" in joined and "min above p1" in joined and "kind 'tap'" in joined


def test_a_table_is_written_in_microseconds_with_its_extremes_and_means():
    text = distribution.yaml_table({"p": [0.0105, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1], "min": 0.001,
                                    "max": 2.5, "means": [0.005, 0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075,
                                                          0.085, 0.095, 1.2345678]}, "meas-ci:session:2026-09-24")
    t = yaml.safe_load(text)
    assert t["p"] == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] and (t["min"], t["max"]) == (1, 2500)
    assert t["means"][-1] == 1234.568 and t["dist"] == "quantiles" and t["source"] == "meas-ci:session:2026-09-24"


def test_a_numpy_sample_gives_the_same_table():
    np = pytest.importorskip("numpy")
    assert distribution.quantile_table(np.arange(100, 0, -1, dtype=float)) == distribution.quantile_table(list(range(1, 101)))


def test_the_batch_tables_regenerate_from_the_pooled_records(repo_root):
    # the compile and background entries' 28 tables are batch_fold_in.py's output on the committed pooled records
    from meas import batch_fold_in
    text = (repo_root / "dataset" / "archetypes.yaml").read_text()
    assert batch_fold_in.rewrite(text, batch_fold_in.load_pools(repo_root)) == text


def test_the_reported_gap_is_the_carried_gap_when_the_phase_start_is_given():
    # the rule reads a component's gap mean from per_thread in the desktop and session pools: given the phase's start
    # it takes the gaps as the carried table does — merged over the threads, wrapped round the phase
    rows = _rows({1: [1.0, 5.0], 2: [3.0]})
    assert campaign.per_thread(rows, 10.0, None, 0.0)["worker"]["gap_ms"]["mean"] == pytest.approx(10.0 / 3 * 1000)


@pytest.mark.parametrize("sample", [[1.0, 2.0, 3.0, 100.0], [50939.0, 51300.0, 52001.0, 53255.0, 54695.0, 55068.0, 59377.0, 59997.0]])
def test_every_interval_mean_lies_inside_its_interval_and_the_table_keeps_the_mean(sample):
    # a small sample's step mass can reach past a linear quantile knot by a fraction of a sample; the table moves that
    # sliver into the neighbouring interval, so each mean lies inside its interval and their weighted sum is the mean
    t = distribution.quantile_table(sample)
    bounds = [t["min"], *t["p"], t["max"]]
    assert all(bounds[i] <= m <= bounds[i + 1] for i, m in enumerate(t["means"]))
    assert sum(w * m for w, m in zip(MASSES, t["means"])) == pytest.approx(sum(sample) / len(sample))
