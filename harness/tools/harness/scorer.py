"""Scorer — docs/harness/metrics.md §9 over aggregates, per the scoring spec's terms.

`score` takes aggregate rows (any number of runs) and a scoring spec and
returns two kinds of rows: one per term per run (the term's identity, its
aggregate under `fixed`, `oracle`, and the run's condition, both improvements,
the share, the weight, the `no_headroom` and `censored` marks) and one per run
for the file's weighted score. Machine schema: `harness/scores/schema/`.

Pairing: a run's `fixed` baseline is the `fixed` run with the same
`workload_id` and `boot_default` (`fixed` carries no table, so it is shared
across tables); its `oracle` is the `oracle` run with the same `workload_id`,
`table`, and `boot_default`. An alternative-default `fixed` run (non-empty
`boot_default`) re-scores the table's `oracle` and every other condition against
itself; those score rows carry the alternative's `boot_default`.

Rules fixed in the Phase 8 spec (decision 4) and the 8.2 spec (decision 4):
a no-headroom term (the oracle's improvement below the aggregate's floor) keeps
its weight and enters the file score as if the condition had captured all of
it (share 1); a `turnaround` term whose task did not complete is scored on the
censored lower bound the aggregates carry (`turnaround_censored`) and marked;
a term whose aggregate is absent stops the scorer.
"""

from fractions import Fraction

from .aggregates import fmt as _fmt

LATENCY_FLOOR_US = Fraction(1000)    # metrics doc §10
FRACTION_FLOOR = Fraction(1, 100)    # metrics doc §10

TERM_AGGREGATE = {("ready_wait", "p99"): "p99", ("job", "miss_rate"): "miss_rate",
                  ("cpu_delivered", "progress"): "progress", ("turnaround", "turnaround"): "turnaround"}
FLOOR = {"p99": LATENCY_FLOOR_US, "turnaround": LATENCY_FLOOR_US,
         "miss_rate": FRACTION_FLOOR, "progress": FRACTION_FLOOR}


def floors_for(latency_floor_us=LATENCY_FLOOR_US, fraction_floor=FRACTION_FLOOR):
    """The floors table with another latency floor (and fraction floor): what the
    RQ0 gate evaluator's floor-band line re-scores with (8.7 spec, decision 11)."""
    lat, frac = Fraction(latency_floor_us), Fraction(fraction_floor)
    return {"p99": lat, "turnaround": lat, "miss_rate": frac, "progress": frac}

IDENTITY = ("workload_id", "condition", "table", "seed", "boot_default")
COLUMNS = IDENTITY + ("level", "entity", "metric", "aggregate", "cause",
                      "window_start_us", "window_end_us", "direction", "weight",
                      "value_fixed", "value_oracle", "value_condition",
                      "improvement_oracle", "improvement_condition", "share",
                      "no_headroom", "censored",
                      "score", "weight_sum", "n_terms", "n_no_headroom", "n_censored")


PLACES = 6                           # decimal places in the scores file


def fmt(x):
    return _fmt(x, PLACES)


class ScoringError(ValueError):
    pass


def _runs(agg_rows):
    runs = {}
    for r in agg_rows:
        key = tuple(str(r.get(k, "")) for k in IDENTITY)
        runs.setdefault(key, {})[(r["entity"], r["metric"], r["aggregate"], r["cause"],
                                  str(r["window_start_us"]), str(r["window_end_us"]))] = Fraction(str(r["value"]))
    return runs


def _term_key(term):
    w = term.get("window") or {}
    return (term["entity"], term["metric"], TERM_AGGREGATE[(term["metric"], term["aggregate"])],
            term.get("cause", ""), str(w.get("start_us", "")), str(w.get("end_us", "")))


def _lookup(run, key, who):
    """The term's aggregate in one run; the censored bound for an unfinished turnaround."""
    if key in run:
        return run[key], False
    if key[2] == "turnaround":
        alt = key[:2] + ("turnaround_censored",) + key[3:]
        if alt in run:
            return run[alt], True
    raise ScoringError(f"{who}: no aggregate for term {key}; every scored entity must produce rows "
                       f"inside the term's window (an empty filter is a scoring-spec mistake)")


def _improve(direction, fixed, value):
    return fixed - value if direction == "lower" else value - fixed


def score(agg_rows, spec, floors=None):
    """(term_rows, file_rows) for every run whose workload has a scoring entry.
    `floors` overrides the no-headroom floors per aggregate (default `FLOOR`,
    the metrics doc §10 constants); the floor-band line passes `floors_for(...)`."""
    floors = FLOOR if floors is None else floors
    runs = _runs(agg_rows)
    files = spec["files"]
    fixed_runs = {(k[0], k[4]): v for k, v in runs.items() if k[1] == "fixed"}
    term_rows, file_rows = [], []
    # every (workload, table, boot_default) group present among non-fixed runs
    groups = sorted({(k[0], k[2], k[4]) for k in runs if k[1] != "fixed"})
    for workload, table, run_boot in groups:
        if workload not in files:
            continue
        terms = files[workload]["terms"]
        conditions = sorted(k for k in runs if k[0] == workload and k[2] == table and k[4] == run_boot)
        # baselines: every fixed run of the workload whose boot_default is the runs' own (""),
        # plus every alternative-default fixed run, each scoring the same runs
        baselines = sorted(b for (w, b) in fixed_runs if w == workload) if run_boot == "" else [run_boot]
        for boot in baselines:
            fixed = fixed_runs.get((workload, boot))
            if fixed is None:
                raise ScoringError(f"{workload}: no fixed run for boot_default {boot!r}")
            oracle_key = (workload, "oracle", table, "", run_boot)
            if oracle_key not in runs:
                raise ScoringError(f"{workload}/{table}: no oracle run to normalise against")
            oracle = runs[oracle_key]
            scored = list(conditions) + [(workload, "fixed", table, "", run_boot)]
            for key in scored:
                run = fixed if key[1] == "fixed" else runs[key]
                identity = dict(zip(IDENTITY, key)); identity["boot_default"] = boot
                total = Fraction(0); wsum = Fraction(0); n_nh = 0; n_c = 0
                for term in terms:
                    tk = _term_key(term)
                    v_fixed, _ = _lookup(fixed, tk, f"{workload} fixed")
                    v_oracle, _ = _lookup(oracle, tk, f"{workload} oracle")
                    v_cond, censored = _lookup(run, tk, f"{workload} {key[1]}")
                    direction = term["direction"]
                    imp_o = _improve(direction, v_fixed, v_oracle)
                    imp_c = _improve(direction, v_fixed, v_cond)
                    no_headroom = abs(imp_o) < floors[tk[2]]
                    share = None if no_headroom else imp_c / imp_o
                    weight = Fraction(str(term["weight"]))
                    wsum += weight
                    total += weight * (Fraction(1) if no_headroom else share)
                    n_nh += int(no_headroom); n_c += int(censored)
                    term_rows.append({**identity, "level": "term", "entity": tk[0], "metric": tk[1],
                                      "aggregate": tk[2], "cause": tk[3],
                                      "window_start_us": tk[4], "window_end_us": tk[5],
                                      "direction": direction, "weight": fmt(weight),
                                      "value_fixed": fmt(v_fixed), "value_oracle": fmt(v_oracle),
                                      "value_condition": fmt(v_cond),
                                      "improvement_oracle": fmt(imp_o), "improvement_condition": fmt(imp_c),
                                      "share": "" if share is None else fmt(share),
                                      "no_headroom": int(no_headroom), "censored": int(censored),
                                      "score": "", "weight_sum": "", "n_terms": "", "n_no_headroom": "", "n_censored": ""})
                file_rows.append({**identity, "level": "file", "entity": "", "metric": "", "aggregate": "",
                                  "cause": "", "window_start_us": "", "window_end_us": "", "direction": "",
                                  "weight": "", "value_fixed": "", "value_oracle": "", "value_condition": "",
                                  "improvement_oracle": "", "improvement_condition": "", "share": "",
                                  "no_headroom": "", "censored": "",
                                  "score": fmt(total), "weight_sum": fmt(wsum), "n_terms": len(terms),
                                  "n_no_headroom": n_nh, "n_censored": n_c})
    key = lambda r: (tuple(str(r[k]) for k in IDENTITY), r["level"] == "term", r["entity"], r["metric"],
                     r["aggregate"], r["cause"], str(r["window_start_us"]))
    return sorted(term_rows, key=key), sorted(file_rows, key=key)
