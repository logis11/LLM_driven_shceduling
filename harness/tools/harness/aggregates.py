"""Aggregates — docs/harness/metrics.md §8, the trace-derived ones, over one run's records.

`compute_aggregates` takes the typed rows of one records file (what
`records.read_csv` returns) and yields aggregate rows: one per
(entity, metric, aggregate, cause, window, index) with a value. Every trace
aggregate §8 lists is here whether a scoring term weights it or not, so the
scorer, the guards, and the report read one file (`harness/aggregates/schema/`).
The recognition aggregates are the grader's (sub-task 8.4), not this module's.

Windows: the whole file always; plus, per (entity, metric), any windows the
scoring spec's terms name — the caller passes them. A window keeps rows whose
anchor `t` lies in the closed interval, as the observation window keeps
observations "at or before" `T_end`.

Two §8 aggregates are not computed here: the per-switch excess and its boost
variant. Both subtract the interactive task's waits outside every switch and
boost window, and the boost windows are sized from the hogs' occupancy
intervals after each boost instant (§8), which records do not carry. They need
boost-window rows from the primitives first; until then the share inside switch
windows is the switch aggregate written.

Values are written as decimal strings at a fixed precision (`fmt`) so identical
records give identical files: twelve places here, because the scorer divides
these values and its own six-place shares must be exact to their last digit
(a six-place progress made an exact −0.5 share read −0.499995). Percentiles are
computed exactly on the integer records with numpy's "linear" convention
(position (n − 1)·p/100 on the sorted values, interpolate between the two
neighbours; R type 7), so no float noise reaches the file.
"""

from decimal import ROUND_HALF_EVEN, Decimal
from fractions import Fraction

import numpy as np
import pandas as pd

T_INTERACTION_US = 100_000          # metrics doc §10
PERCENTILE_METHOD = "linear"        # numpy's linear interpolation, R type 7 (metrics doc §8)
PLACES = 12                         # decimal places in the aggregates file

IDENTITY = ("workload_id", "condition", "table", "seed", "boot_default")
COLUMNS = IDENTITY + ("entity", "metric", "aggregate", "cause",
                      "window_start_us", "window_end_us", "index", "value")
PROVENANCES = ("unmodified", "clamped", "held", "fallback")


def fmt(x, places=PLACES) -> str:
    """A number as a decimal string with `places` places, exactly rounded (half to even)."""
    if isinstance(x, Fraction):
        d = Decimal(x.numerator) / Decimal(x.denominator)
    elif isinstance(x, (int, np.integer)):
        d = Decimal(int(x))
    else:
        d = Decimal(repr(float(x)))
    return format(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN), "f")


def percentile(values, p) -> Fraction:
    """The p-th percentile by numpy's `linear` method, computed exactly on the sorted values."""
    v = sorted(int(x) for x in values)
    if not v:
        raise ValueError("percentile of no values")
    h = Fraction(len(v) - 1) * Fraction(p, 100)
    k = int(h)                                   # floor; h ≥ 0
    if k + 1 >= len(v):
        return Fraction(v[-1])
    return Fraction(v[k]) + (h - k) * (v[k + 1] - v[k])


def run_identity(rows) -> dict:
    ids = {tuple(str(r.get(k, "")) for k in IDENTITY) for r in rows}
    if len(ids) != 1:
        raise ValueError(f"records of more than one run: {sorted(ids)}")
    return dict(zip(IDENTITY, next(iter(ids))))


def _in_window(t, window):
    start, end = window
    return (start is None or t >= start) and (end is None or t <= end)


def compute_aggregates(rows, windows=None):
    """Aggregate rows for one run. `windows`: {(entity, metric): [(start_us, end_us), …]}."""
    windows = windows or {}
    identity = run_identity(rows)
    df = pd.DataFrame(rows)
    for col in ("cause", "provenance", "algorithm", "index", "period_us"):
        if col not in df.columns:
            df[col] = np.nan
    out = []

    def emit(entity, metric, aggregate, value, cause="", window=(None, None), index=""):
        start, end = window
        out.append({**identity, "entity": entity, "metric": metric, "aggregate": aggregate,
                    "cause": cause,
                    "window_start_us": "" if start is None else str(start),
                    "window_end_us": "" if end is None else str(end),
                    "index": "" if index == "" else str(index),
                    "value": fmt(value)})

    busy = df[df["metric"] == "busy"]
    t_end = int(busy["t"].iloc[0]) if len(busy) else None

    def windows_for(entity, metric):
        return [(None, None)] + list(windows.get((entity, metric), []))

    # --- ready_wait: per entity, per cause (and any cause), per window
    rw = df[df["metric"] == "ready_wait"]
    for entity, g in rw.groupby("entity", sort=True):
        causes = [""] + sorted(c for c in g["cause"].dropna().unique())
        for window in windows_for(entity, "ready_wait"):
            for cause in causes:
                sel = g if cause == "" else g[g["cause"] == cause]
                sel = sel[[_in_window(int(t), window) for t in sel["t"]]]
                if sel.empty:
                    continue
                vals = sel["value"].astype(int).tolist()
                emit(entity, "ready_wait", "count", len(vals), cause, window)
                emit(entity, "ready_wait", "mean", Fraction(sum(vals), len(vals)), cause, window)
                for p, name in ((50, "p50"), (95, "p95"), (99, "p99")):
                    emit(entity, "ready_wait", name, percentile(vals, p), cause, window)
                emit(entity, "ready_wait", "max", max(vals), cause, window)
                over = sum(1 for v in vals if v > T_INTERACTION_US)
                emit(entity, "ready_wait", "over_threshold", Fraction(over, len(vals)), cause, window)

    # --- job: per entity, per window
    jobs = df[df["metric"] == "job"]
    for entity, g in jobs.groupby("entity", sort=True):
        for window in windows_for(entity, "job"):
            sel = g[[_in_window(int(t), window) for t in g["t"]]]
            if sel.empty:
                continue
            vals = sel["value"].astype(int).tolist()
            periods = sel["period_us"].astype(int).tolist()
            emit(entity, "job", "count", len(vals), "", window)
            missed = sum(1 for v, per in zip(vals, periods) if v > per)
            emit(entity, "job", "miss_rate", Fraction(missed, len(vals)), "", window)
            emit(entity, "job", "latency_p50", percentile(vals, 50), "", window)
            emit(entity, "job", "latency_p99", percentile(vals, 99), "", window)

    # --- lifetime rows: progress, completion, turnaround (and the censored bound), preempts
    per_entity = {}
    for metric in ("cpu_delivered", "demand", "completed", "turnaround", "preempt_count"):
        for _, r in df[df["metric"] == metric].iterrows():
            per_entity.setdefault(r["entity"], {})[metric] = (int(r["t"]), int(r["value"]))
    arrivals = {r["entity"]: int(r["t"]) for _, r in rw[rw["cause"] == "arrive"].iterrows()}
    lane_preempts = 0
    for entity in sorted(per_entity):
        m = per_entity[entity]
        if "cpu_delivered" in m and "demand" in m and m["demand"][1] > 0:
            emit(entity, "cpu_delivered", "progress", Fraction(m["cpu_delivered"][1], m["demand"][1]))
        if "completed" in m:
            emit(entity, "completed", "completion", m["completed"][1])
        if "turnaround" in m:
            emit(entity, "turnaround", "turnaround", m["turnaround"][1])
        elif "completed" in m and m["completed"][1] == 0 and entity in arrivals and t_end is not None:
            emit(entity, "turnaround", "turnaround_censored", t_end - arrivals[entity])
        if "preempt_count" in m:
            emit(entity, "preempt_count", "preempt_count", m["preempt_count"][1])
            lane_preempts += m["preempt_count"][1]
    if any("preempt_count" in m for m in per_entity.values()):
        emit("lane", "preempt_count", "preempt_count", lane_preempts)

    # --- config_interval: provenance shares, fallback share, config age
    ci = df[df["metric"] == "config_interval"]
    if len(ci):
        vals = ci["value"].astype(int).tolist()
        total = sum(vals)
        n = len(vals)
        for prov in PROVENANCES:
            sel = ci[ci["provenance"] == prov]
            t_share = Fraction(int(sel["value"].astype(int).sum()), total) if total else Fraction(0)
            emit("schedule", "config_interval", f"time_share_{prov}", t_share)
            emit("schedule", "config_interval", f"count_share_{prov}", Fraction(len(sel), n))
        fb = ci[ci["provenance"].isin(["fallback", "held"])]
        emit("schedule", "config_interval", "fallback_share",
             Fraction(int(fb["value"].astype(int).sum()), total) if total else Fraction(0))
        emit("schedule", "config_interval", "config_age_count", n)
        emit("schedule", "config_interval", "config_age_mean", Fraction(total, n))
        for p, name in ((50, "config_age_p50"), (99, "config_age_p99")):
            emit("schedule", "config_interval", name, percentile(vals, p))
        emit("schedule", "config_interval", "config_age_max", max(vals))

    # --- switch_window: share of the window inside switch windows
    sw = df[df["metric"] == "switch_window"]
    if len(sw) and t_end:
        inside = sum(min(int(v), t_end - int(t)) for t, v in zip(sw["t"], sw["value"]))
        emit("schedule", "switch_window", "share_inside_switch_windows", Fraction(inside, t_end))

    # --- busy: utilisation and idle
    if t_end:
        b = int(busy["value"].iloc[0])
        emit("lane", "busy", "utilisation", Fraction(b, t_end))
        emit("lane", "busy", "idle", t_end - b)
        emit("lane", "busy", "t_end", t_end)

    out.sort(key=sort_key)
    return out


def sort_key(row):
    return (row["entity"], row["metric"], row["aggregate"], row["cause"],
            int(row["window_start_us"] or -1), int(row["window_end_us"] or -1),
            int(row["index"] or -1))
