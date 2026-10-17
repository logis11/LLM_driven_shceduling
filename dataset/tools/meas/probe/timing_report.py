#!/usr/bin/env python3
"""Compare replayed key timing (replay.py log) with delivered timing
(xkeylog.py log). Prints a JSON summary: counts, requested vs delivered
inter-key gaps, error percentiles in ms."""

import json
import statistics
import sys


def load(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def pct(values, q):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


sent = load(sys.argv[1])
got = load(sys.argv[2])
req = [s["gap_ms"] for s in sent[1:]]
sent_gaps = [(b["sent_us"] - a["sent_us"]) / 1000 for a, b in zip(sent, sent[1:])]
got_gaps = [(b["mono_us"] - a["mono_us"]) / 1000 for a, b in zip(got, got[1:])]
n = min(len(req), len(got_gaps))
err = [got_gaps[i] - req[i] for i in range(n)]
abs_err = [abs(e) for e in err]
print(json.dumps({
    "n_sent": len(sent), "n_delivered": len(got),
    "requested_gap_ms": {"p50": pct(req, .5), "p90": pct(req, .9)},
    "sent_gap_ms": {"p50": pct(sent_gaps, .5), "p90": pct(sent_gaps, .9)},
    "delivered_gap_ms": {"p50": pct(got_gaps, .5), "p90": pct(got_gaps, .9)},
    "abs_error_ms": {"p50": pct(abs_err, .5), "p90": pct(abs_err, .9),
                     "p99": pct(abs_err, .99), "max": max(abs_err) if abs_err else None},
    "mean_error_ms": statistics.fmean(err) if err else None,
}, indent=1))
