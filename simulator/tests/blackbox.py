"""Shared plumbing of the black-box unit tests on the binary: run a hand workload through the
invocation contract's flags (data-contracts §11, contract 10) and read the trace back.

The tests import it from their own directory; it holds no assertion of its own.
"""
import json
import os
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_SIM = os.path.join(ROOT, "simulator", "src", "sim")
SLICE = 10000
# The boot default (harness/boot-defaults/ostep.json) and the other three algorithms at the same
# granularity (recognition-vocabulary §2)
PARAMS = {
    "MLFQ": {"num_queues": 3, "timeslice_us": SLICE, "timeslice_growth": 2, "boost_interval_us": 100000},
    "FIFO": {},
    "EDF": {"residual_timeslice_us": SLICE},
    "LOTTERY": {"timeslice_us": SLICE, "batch_share": 0.15},
}
ALGORITHMS = ("MLFQ", "FIFO", "EDF", "LOTTERY")


def sim_path(argv):
    return argv[1] if len(argv) > 1 else DEFAULT_SIM


def entry(algorithm, cap=None, t=0, provenance="fallback"):
    return {"t_us": t, "config": {"algorithm": algorithm, "params": PARAMS[algorithm], "batch_bandwidth_cap": cap},
            "provenance": provenance}


def run(sim, name, events, entries, condition="fixed"):
    """The trace of `events` under the schedule `entries`, every line parsed. Raises on a non-zero exit."""
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, "w.json"); s = os.path.join(d, "s.json"); t = os.path.join(d, "t.jsonl")
        with open(w, "w") as f:
            json.dump({"meta": {"id": name}, "ground_truth": {}, "events": events}, f)
        with open(s, "w") as f:
            json.dump({"workload_id": name, "condition": condition, "schedule": entries}, f)
        run_files(sim, w, s, t)
        return read(t)


def run_files(sim, workload, schedule, trace):
    p = subprocess.run([sim, "--workload", workload, "--schedule", schedule, "--out-trace", trace],
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"{sim} exit {p.returncode}: {p.stderr.strip()}")


def read(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def occupancies(trace):
    """(task, start, end, reason) for every run_start … run_end pair, in trace order (one lane)."""
    out, open_ = [], None
    for e in trace:
        if e["event"] == "run_start":
            open_ = (e["task"], e["t"])
        elif e["event"] == "run_end" and open_ is not None:
            out.append((open_[0], open_[1], e["t"], e["reason"]))
            open_ = None
    return out


def runnable_intervals(trace, task):
    """[start, end) spans over which `task` is runnable: from the ready line that makes it runnable to
    the run_end that blocks or ends it (a preemption keeps it runnable), or its task_end."""
    spans, since = [], None
    for e in trace:
        if e.get("task") != task:
            continue
        if e["event"] == "ready" and since is None:
            since = e["t"]
        elif since is not None and ((e["event"] == "run_end" and e["reason"] != "preempt")
                                    or e["event"] == "task_end"):
            spans.append((since, e["t"]))
            since = None
    return spans


def cpu(trace, task):
    return sum(end - start for t, start, end, _ in occupancies(trace) if t == task)


def cpu_reached(trace, task, amount):
    """The instant `task`'s lane time first reaches `amount` µs, or None."""
    got = 0
    for t, start, end, _ in occupancies(trace):
        if t != task:
            continue
        if got + (end - start) >= amount:
            return start + (amount - got)
        got += end - start
    return None


def parks(trace, task):
    return [e["t"] for e in trace if e["event"] == "x_cap_park" and e["task"] == task and e["in"]]


def kept(trace):
    """The lines the harness reads (data-contracts §9: x_ lines ignored)."""
    return [e for e in trace if not e["event"].startswith("x_")]


def main(tests, argv):
    """Run each (name, function(sim) -> summary) and print one line per test; exit 1 on any failure."""
    import sys
    sim = sim_path(argv)
    ok = True
    for name, t in tests:
        try:
            print(f"test {name}: ok — {t(sim)}")
        except AssertionError as e:
            ok = False
            print(f"test {name}: FAIL — {e}")
        except RuntimeError as e:
            ok = False
            print(f"test {name}: ERROR — {e}")
    sys.stdout.flush()
    return 0 if ok else 1
