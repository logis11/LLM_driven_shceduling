"""The configuration search (11.4 spec, decisions 3–13): the grid the committed search spec expands to, the point's
table, a point's quantity, the three findings and the best point's tie rule, the g band, the boot defaults, the
LOTTERY flag, the route, the checks' line comparison, and the lint."""

import copy
import gzip
from fractions import Fraction

import pytest
import yaml

from conftest import REPO
from harness import search
from harness.drivertable import compose_row

SPEC = REPO / "harness" / "experiments" / "rq0-config-search.yaml"
BUILD = REPO / "dataset" / "build" / "coreset-single"
needs_build = pytest.mark.skipif(not BUILD.exists(), reason="compiled coreset absent")
FLOORS = search.scorer.floors_for()
P99 = {"entity": "editor", "metric": "input_latency", "aggregate": "p99", "direction": "lower", "weight": "1.000000"}
TURN = {"entity": "batch", "metric": "turnaround", "aggregate": "turnaround", "direction": "lower",
        "weight": "0.500000"}


def _spec():
    return search.load_spec(SPEC)


# ------------------------------------------------------------------ the grid

def test_the_committed_grid_is_decision_8s():
    points = search.expand_grid(_spec()["grid"])
    by_alg = {}
    for p in points:
        by_alg[p.config["algorithm"]] = by_alg.get(p.config["algorithm"], 0) + 1
    assert len(points) == 470 and by_alg == {"MLFQ": 288, "LOTTERY": 110, "EDF": 66, "FIFO": 6}
    assert len({p.id for p in points}) == 470 and len({p.key for p in points}) == 470
    assert [p.order for p in points] == list(range(470))
    lottery = [p.config for p in points if p.config["algorithm"] == "LOTTERY"]
    pairs = {(c["batch_bandwidth_cap"], c["params"]["batch_share"]) for c in lottery}
    assert pairs == {(0.05, 0.05), (0.2, 0.2), (0.333, 0.333), (0.5, 0.5), (0.95, 0.9),
                     (None, 0.05), (None, 0.2), (None, 0.333), (None, 0.5), (None, 0.9)}
    moved = [p.config["params"] for p in points if p.config["algorithm"] == "MLFQ"
             and (p.config["params"]["num_queues"] != 3 or p.config["params"]["timeslice_growth"] != 2)]
    assert len(moved) == 24 and all(m["timeslice_us"] == 10000 and m["boost_interval_us"] == 100000 for m in moved)


def test_every_points_table_composes_to_the_point():
    spec = _spec()
    prior = yaml.safe_load((REPO / spec["pins"]["driver_table"]["path"]).read_text())
    for p in search.expand_grid(spec["grid"]):
        table = search.point_table(prior, p.config)
        assert table["role"] == "prior" and len(table["rows"]) == len(prior["rows"])
        assert {compose_row(r) for r in table["rows"]} == {p.key}


def test_point_ids_name_the_configuration():
    assert search.point_id({"algorithm": "MLFQ", "batch_bandwidth_cap": None, "params": {
        "num_queues": 3, "timeslice_us": 10000, "timeslice_growth": 2, "boost_interval_us": 100000}}) \
        == "mlfq-s10000-b100000-q3-x2-cnone"
    assert search.point_id({"algorithm": "LOTTERY", "batch_bandwidth_cap": 0.95,
                            "params": {"batch_share": 0.9, "timeslice_us": 700}}) == "lottery-s700-w0.9-c0.95"
    assert search.point_id({"algorithm": "FIFO", "batch_bandwidth_cap": 0.333, "params": {}}) == "fifo-c0.333"


@needs_build
def test_the_committed_spec_lints_clean_and_holds_the_points_it_names():
    spec = _spec()
    assert search.lint_spec(spec, REPO, BUILD) == []
    plan = search.plan(spec, REPO, BUILD)
    assert plan.fixed == "mlfq-s10000-b100000-q3-x2-cnone"
    assert plan.alternatives["ostep-slice-500us"] == "mlfq-s500-b100000-q3-x2-cnone"
    assert len(plan.prior) == 8 and len(set(plan.prior)) == 8
    assert plan.rows["c7-gaming"] == "edf-s10000-c0.05"
    assert plan.rows["c1-transcode"] == "lottery-s10000-w0.333-c0.333"


@needs_build
def test_the_lint_refuses_a_count_the_blocks_do_not_give_and_a_missing_boot_default():
    spec = _spec()
    bad = copy.deepcopy(spec)
    bad["grid"]["points"] = 469
    assert any("expand to 470" in e for e in search.lint_spec(bad, REPO, BUILD))
    bad = copy.deepcopy(spec)
    bad["grid"]["blocks"][0]["cross"]["timeslice_us"].remove(10000)
    errors = search.lint_spec(bad, REPO, BUILD)
    assert any("the boot default ostep is not a point" in e for e in errors)
    assert any("prior table's configuration" in e for e in errors)
    bad = copy.deepcopy(spec)
    bad["pins"]["scoring_spec"]["sha256"] = "0" * 64
    assert any(e.startswith("pins/scoring_spec") for e in search.lint_spec(bad, REPO, BUILD))
    bad = copy.deepcopy(spec)
    bad["grid"]["blocks"][3]["cross"]["residual_timeslice_us"].append(100)
    assert any("not a legal configuration" in e for e in search.lint_spec(bad, REPO, BUILD))


# ------------------------------------------------------------------ the quantity

def test_a_terms_reading_is_signed_and_zero_under_the_floor():
    f = Fraction(1000)
    assert search.term_reading("lower", Fraction(10000), Fraction(9001), f) == (Fraction(999), 0, "under")
    assert search.term_reading("lower", Fraction(10000), Fraction(9000), f) == (Fraction(1000), Fraction(1, 10),
                                                                              "better")
    assert search.term_reading("lower", Fraction(10000), Fraction(12000), f) == (Fraction(-2000), Fraction(-1, 5),
                                                                               "worse")
    assert search.term_reading("lower", Fraction(10000), Fraction(10999), f)[1] == 0
    with pytest.raises(search.SearchError):
        search.term_reading("lower", Fraction(0), Fraction(1, 10), Fraction(1, 100))


def test_the_quantity_is_the_weighted_mean_the_picks_were_read_in():
    """c1-transcode's row on the corrected runs: the editor's P99 447,969.18 → 430,531.08 µs (weight 1), the
    batch's turnaround 3,894,612,815 → 4,134,853,844 µs (weight 0.5): the 11.4 spec's 0.005."""
    terms = [{**P99, "entity": "video-editor", "metric": "app_latency"}, TURN]
    q, readings = search.quantity(terms, [Fraction("447969.18"), Fraction(3894612815)],
                                  [Fraction("430531.08"), Fraction(4134853844)], FLOORS)
    assert round(float(q), 3) == 0.005
    assert q == ((Fraction("447969.18") - Fraction("430531.08")) / Fraction("447969.18")
                 + Fraction(1, 2) * (Fraction(3894612815) - Fraction(4134853844)) / Fraction(3894612815)) / Fraction(3, 2)
    assert [r["against_floor"] for r in readings] == ["better", "worse"]


# ------------------------------------------------------------------ the findings

ORDER = {p: i for i, p in enumerate(["boot", "row", "a", "b", "c"])}


def _find(values, row="row", fixed="boot", g=Fraction(1, 2), terms=(P99,)):
    return search.find({k: [Fraction(x) for x in v] for k, v in values.items()}, ORDER, list(terms), row, fixed, g,
                       FLOORS)


def test_finding_1_when_no_two_points_differ_by_the_floor():
    r = _find({"boot": [10000], "row": [10500], "a": [9600], "b": [10099]})
    assert r["finding"] == 1 and r["spread"][0]["range"] == 900
    assert _find({"boot": [10000], "row": [10500], "a": [9500]})["finding"] == 2       # a range of 1,000: spread


def test_finding_3_when_the_row_is_worse_than_the_boot_default_by_the_floor():
    r = _find({"boot": [10000], "row": [12000], "a": [10500]})
    assert r["finding"] == 3 and r["best"] == "boot" and r["row_quantity"] == Fraction(-1, 5)
    assert r["best_better_on"] == ["editor"]


def test_finding_3_when_the_row_captures_at_most_1_minus_g_of_the_best():
    r = _find({"boot": [100000], "row": [80000], "a": [55000], "b": [60000]})
    assert r["best"] == "a" and r["finding"] == 3            # 0.2 ≤ 0.5 × 0.45
    assert _find({"boot": [100000], "row": [80000], "a": [55000]}, g=Fraction(67, 100))["finding"] == 2   # 0.2 > 0.33 × 0.45


def test_finding_2_when_the_row_holds_the_spread():
    assert _find({"boot": [100000], "row": [50000], "a": [45000], "b": [90000]})["finding"] == 2


def test_the_row_wins_a_tie_for_the_best():
    """c7-gaming's shape: the row at a miss rate of 0, other points too — the row is the best, not finding 3."""
    terms = [{"entity": "game.chain.1", "metric": "job", "aggregate": "miss_rate", "direction": "lower",
              "weight": "1.000000"}]
    r = _find({"boot": ["1"], "a": ["0"], "row": ["0"], "b": ["0.5"]}, terms=terms)
    assert r["tied"] == ["row", "a"] and r["best"] == "row" and r["finding"] == 2


def test_a_tie_without_the_row_goes_to_the_first_in_the_grids_order():
    r = _find({"boot": [100000], "row": [100000], "c": [40000], "b": [40000]})
    assert r["tied"] == ["b", "c"] and r["best"] == "b"


def test_equal_quantities_at_zero_do_not_make_finding_3():
    """The row under the floor of fixed and a point under it the other way: both read 0, the row best by the tie."""
    r = _find({"boot": [10000], "row": [10900], "a": [9100]})
    assert r["best"] == "row" and r["finding"] == 2


# ------------------------------------------------------------------ a file's reading

def _plan(points, row, fixed="mlfq-boot", alternatives=None, terms=(P99,)):
    spec = {"reading": {"g": 0.5, "g_band": [0.25, 0.33, 0.5, 0.67], "floors": {"latency_us": 1000, "fraction": 0.01},
                        "lottery_flag": True},
            "boot_defaults": {"primary": "ostep", "alternatives": list(alternatives or {})},
            "route": {"table_rewrite": "the table is rewritten", "workload_redesign": "workload redesign"}}
    pts = [search.Point(pid, i, {"algorithm": alg, "params": {}, "batch_bandwidth_cap": None})
           for i, (pid, alg) in enumerate(points)]
    return search.Plan(spec=spec, points=pts, by_key={}, files=["w"], workloads={}, rows={"w": row}, fixed=fixed,
                       alternatives=dict(alternatives or {}), prior=[row, "mlfq-boot"], prior_doc={"role": "prior"},
                       scoring_spec={"files": {"w": {"terms": [{"entity": t["entity"], "metric": t["metric"],
                                                                 "aggregate": t["aggregate"],
                                                                 "direction": t["direction"],
                                                                 "weight": float(Fraction(t["weight"]))}
                                                                for t in terms]}}})


def _outcomes(values, out=()):
    return {pid: {"terms": [{"entity": "editor", "metric": "input_latency", "aggregate": "p99", "direction": "lower",
                             "weight": "1.000000", "value": str(v), "censored": 0}],
                  "out": (["starvation_floor: x"] if pid in out else [])} for pid, v in values.items()}


def test_a_files_reading_with_its_band_its_boot_defaults_and_the_lottery_flag():
    plan = _plan([("mlfq-boot", "MLFQ"), ("mlfq-row", "MLFQ"), ("mlfq-alt", "MLFQ"), ("lottery-a", "LOTTERY"),
                  ("edf-b", "EDF")], row="mlfq-row", alternatives={"ostep-slice-500us": "mlfq-alt"})
    r = search.read_file("w", _outcomes({"mlfq-boot": 100000, "mlfq-row": 70000, "mlfq-alt": 70000,
                                         "lottery-a": 45000, "edf-b": 60000}), plan)
    assert r["finding"] == 2 and r["best"] == "lottery-a"           # 0.3 > 0.5 × 0.55
    # 0.3 ≤ 0.75 × 0.55 and ≤ 0.67 × 0.55, > 0.5 × 0.55 and > 0.33 × 0.55
    assert r["g_band"] == {"0.25": 3, "0.33": 3, "0.5": 2, "0.67": 2} and r["g_range"] == "2–3"
    assert r["boot_defaults"]["ostep-slice-500us"]["finding"] == 3     # fixed at 70,000: the row 0
    assert r["boot_range"] == "2–3"
    assert r["prior_at_least_row"] == 1 and r["prior_read"] == 2
    assert r["lottery"]["removed"] == 1 and r["lottery"]["finding_without"] == 2
    assert r["lottery"]["changes"] == {"g 0.33": 2}                    # edf-b's 0.4: 0.3 > 0.67 × 0.4


def test_a_point_out_of_the_reading_is_no_candidate_and_a_boot_default_out_gives_no_reading():
    plan = _plan([("mlfq-boot", "MLFQ"), ("mlfq-row", "MLFQ"), ("mlfq-alt", "MLFQ"), ("edf-b", "EDF")],
                 row="mlfq-row", alternatives={"ostep-slice-100000us": "mlfq-alt"})
    r = search.read_file("w", _outcomes({"mlfq-boot": 100000, "mlfq-row": 90000, "mlfq-alt": 10, "edf-b": 20000},
                                        out=("mlfq-alt", "edf-b")), plan)
    assert r["read"] == 2 and [o["point"] for o in r["out"]] == ["mlfq-alt", "edf-b"]
    assert r["finding"] == 2 and r["best"] == "mlfq-row"
    assert r["boot_defaults"]["ostep-slice-100000us"]["finding"] is None
    r = search.read_file("w", _outcomes({"mlfq-boot": 100000, "mlfq-row": 90000, "mlfq-alt": 10, "edf-b": 1},
                                        out=("mlfq-row",)), plan)
    assert r["finding"] is None and "row" in r["no_reading"]


def test_the_route_is_one():
    spec = _plan([], row="r").spec
    files = [{"workload_id": "a", "finding": 2, "g_band": {"0.5": 2}, "boot_defaults": {"ostep": {"finding": 2}}},
             {"workload_id": "b", "finding": 3, "g_band": {"0.5": 3}, "boot_defaults": {"ostep": {"finding": 3}}}]
    r = search.route(files, spec)
    assert r["route"] == "the table is rewritten" and r["files_at_3"] == ["b"]
    files[1]["finding"] = 1
    assert search.route(files, spec)["route"] == "workload redesign"
    files[1]["finding"] = None
    assert search.route(files, spec)["route"] is None


# ------------------------------------------------------------------ the checks

def _trace(tmp_path, name, lines):
    p = tmp_path / name
    with gzip.open(p, "wb") as f:
        f.write(("\n".join(lines) + "\n").encode())
    return p


def test_the_fixed_check_compares_the_traces_but_the_set_aside_lines(tmp_path):
    point = _trace(tmp_path, "p.gz", ['{"event":"meta","condition":"oracle"}',
                                      '{"event":"config_applied","t":0,"index":0}',
                                      '{"event":"config_applied","t":0,"index":1}',
                                      '{"event":"run_start","t":0,"task":"a"}',
                                      '{"event":"config_applied","t":2000000,"index":2}',
                                      '{"event":"run_end","t":3000000,"task":"a"}'])
    ref = _trace(tmp_path, "f.gz", ['{"event":"meta","condition":"fixed"}',
                                    '{"event":"config_applied","t":0,"index":0}',
                                    '{"event":"run_start","t":0,"task":"a"}',
                                    '{"event":"x_mlfq_boost","t":2000000}',
                                    '{"event":"run_end","t":3000000,"task":"a"}'])
    aside = ["meta", "config_applied", "x_config_pending"]
    r = search.compare_lines(point, ref, aside)
    assert not r["equal"] and r["first_difference"]["line"] == 2
    assert search.applied_after_boot(point) == [2000000]
    assert search.compare_lines(point, ref, aside, [2000000])["equal"]
