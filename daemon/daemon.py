#!/usr/bin/env python3
"""The recognition daemon — a running skeleton.

    daemon.py --workload WORKLOAD.json --condition fixed|oracle|random
              --telemetry focus|names
              --driver-table TABLE.yaml --boot-default BOOT.json
              --out-schedule SCHEDULE.json --out-log LOG.json [--seed N]

One invocation is one run: one workload file x one condition x one telemetry
shape x (for a drawing condition) one seed. Every flag is required, there are no
positional arguments and no defaults, the two outputs are written only to the
paths given, and exit 0 means both were written (the invocation contract,
`docs/data-contracts.md` §11; the 2026-09-11 memo). Nothing is written to
standard output; diagnostics go to standard error.

The pipeline is the one the daemon guide draws (`docs/daemon/daemon-guide.md` §1):

    workload --> visible projection --> telemetry snapshots --> recognizer
             --> validator --> config mapper --> config schedule + recognition log

What this skeleton implements: the three conditions the RQ0 run needs that take
no model — `fixed` (the boot default alone), `oracle` (reads the answer key) and
`random` (a seeded draw over the driver table's rows). The five remaining
conditions of the guide's §4 table — `shipped_catalogue`, `strongest_name_table`,
`llm_vocab`, `llm_algo`, `llm_full` — are refused with a non-zero exit, as rule 9
of the invocation contract asks, and each is one `Recognizer` away: the seat is
`RECOGNIZERS` below, a function from a telemetry snapshot to a proposal.

Not here, and deliberately: no LLM client, no record/replay store, no hold time
or hysteresis, and no clamping path. The validator seat exists and the three
conditions above pass through it, but since their proposals are composed from the
driver table they are valid by construction, so only `unmodified` and `fallback`
are ever emitted. A `clamped` or `held` answer needs the recognizer that can
produce one.

Verified byte-identical to the harness's reference mock
(`harness/tools/tests/mocks/daemon.py`) over the core set under all three
conditions and both telemetry shapes; see `README.md`.
"""

import argparse
import json
import pathlib
import random
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "tools"))

from drivertable.config_schema import ALGORITHMS, CAP_RANGE, check_params  # noqa: E402

try:
    import yaml
except ImportError:                                    # pragma: no cover
    yaml = None

CONDITIONS = ("fixed", "oracle", "random")
UNIMPLEMENTED = ("shipped_catalogue", "strongest_name_table",
                 "llm_vocab", "llm_algo", "llm_full")
DRAWING = ("random",)                   # the conditions that take a seed
TELEMETRY = ("focus", "names")          # the shapes of §5 rule 6


class DaemonError(ValueError):
    """A refused invocation or an unusable input: the caller exits non-zero."""


# ----------------------------------------------------- the visible projection

def projection(doc) -> dict:
    """The visible projection (`docs/data-contracts.md` §4, "The two derived
    views"): one entry per canonical task, each with the name the recognizer
    sees, its declared class and its pinned lifetime times, plus the focus
    intervals the focus track gives it. A spawn table's children are folded by
    name and class under their parent — they enter telemetry with the parent and
    never leave. `ground_truth` is not read here: only the oracle may read it,
    and it reads it from the document itself.
    """
    focus = defaultdict(list)
    for win in doc.get("focus") or []:
        focus[win["task"]].append({"t_start": int(win["t_start"]), "t_end": int(win["t_end"])})
    tasks = []
    for ev in doc.get("events", []):
        if ev.get("op") != "arrive":
            continue
        task = {"name": ev["name"], "declared_class": ev["declared_class"],
                "t_arrive": int(ev["t"])}
        if ev.get("depart") is not None:
            task["t_depart"] = int(ev["depart"])
        if ev["id"] in focus:
            task["focus"] = sorted(focus[ev["id"]], key=lambda w: w["t_start"])
        if ev.get("spawn_table"):
            counts = Counter((c["name"], c["declared_class"]) for c in ev["spawn_table"])
            task["children"] = [{"name": n, "declared_class": k, "count": c}
                                for (n, k), c in sorted(counts.items())]
        tasks.append(task)
    return {"workload_id": workload_id(doc), "tasks": tasks}


def workload_id(doc) -> str:
    return (doc.get("meta") or {}).get("id") or doc.get("workload_id") or ""


# ------------------------------------------------------------- telemetry (§5)

def snapshots(proj, telemetry="focus") -> list:
    """The telemetry snapshots, one per pinned instant at which the set changed,
    under the six rules of `docs/data-contracts.md` §5:

    1. the set is the name->count multiset, so a count-only change is a change;
    2. every pinned event at one instant is applied first and yields one snapshot;
    3. `processes` is sorted by name, so reruns are byte-identical;
    4. the snapshot at the final instant is emitted like any other — the
       projection carries no duration and the daemon cannot know it is the end;
    5. nothing else emits: no timers, no periodic re-asks;
    6. the set also holds the focus holder, so a focus change is a set change,
       while a move between two instances of one name changes nothing.

    `telemetry` is the shape shown to the recognizer, `focus` (the holder beside
    the multiset) or `names` (the multiset alone). The query points are the same
    under both, because they are defined on the full set; under `names` a
    focus-only change repeats the previous snapshot byte for byte.
    """
    if telemetry not in TELEMETRY:
        raise DaemonError(f"telemetry shape {telemetry!r}: one of {', '.join(TELEMETRY)}")
    deltas = defaultdict(Counter)
    gains, losses = defaultdict(list), defaultdict(list)
    for task in proj["tasks"]:
        deltas[task["t_arrive"]][task["name"]] += 1
        for child in task.get("children", []):
            deltas[task["t_arrive"]][child["name"]] += child["count"]
        if "t_depart" in task:
            deltas[task["t_depart"]][task["name"]] -= 1
        for win in task.get("focus", []):
            gains[win["t_start"]].append(task["name"])
            losses[win["t_end"]].append(task["name"])
    live, holder = Counter(), None
    out = []
    for t in sorted(set(deltas) | set(gains) | set(losses)):
        before = (dict(live), holder)
        live.update(deltas.get(t, {}))
        live = Counter({n: c for n, c in live.items() if c > 0})
        if losses.get(t):          # the intervals never overlap: an end at t precedes a start at t
            holder = None
        if gains.get(t):
            holder = gains[t][0]
        if (dict(live), holder) == before:
            continue
        snap = {"t_us": t, "processes": [{"name": n, "count": c} for n, c in sorted(live.items())]}
        if telemetry == "focus":
            snap["focus"] = holder
        out.append(snap)
    return out


# ------------------------------------------------------------- driver table

def read_driver_table(path):
    """The driver table indexed by (mode, background_wanted). The table is
    인지오's artifact and this tree only reads it; its shape is checked by
    `make lint`, not here."""
    if yaml is None:
        raise DaemonError("PyYAML is needed to read the driver table "
                          "(pip install -r tools/requirements.txt)")
    try:
        doc = yaml.safe_load(pathlib.Path(path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise DaemonError(f"driver table {path}: {exc}") from exc
    rows = {}
    for row in (doc or {}).get("rows") or []:
        rows[(row["mode"], bool(row["background_wanted"]))] = row
    if not rows:
        raise DaemonError(f"driver table {path}: no rows")
    return rows


def compose(row) -> dict:
    """The configuration a `system`-only condition receives from a row: the row's
    default algorithm, that entry's params, and the row's cap (§10).

    Composed through the **canonical bytes** — `sort_keys=True`, every key in one
    order — because that string is what `tools/drivertable/lint.py`'s `compose`
    and the harness's `compose_row` produce, and what the pair check between them
    pins. Writing the dict out in insertion order instead would put the same
    configuration in the schedule under a different spelling."""
    algorithm = row["default"]
    config = {"algorithm": algorithm,
              "params": row["entries"][algorithm]["params"],
              "batch_bandwidth_cap": row["batch_bandwidth_cap"]}
    return json.loads(json.dumps(config, sort_keys=True, separators=(",", ":")))


# --------------------------------------------------------- the recognizer seat

def recognize_fixed(_snap, _ctx):
    """`fixed` consults no recognizer at all: it is the control condition, the
    boot default for the whole run. It never reaches here — `run` returns its
    one-entry schedule before the walk — and is listed so the table of
    conditions is complete."""
    return None, None


def recognize_oracle(snap, ctx):
    """`oracle` reads the answer key: the ground-truth segment covering the query
    point gives the mode and the attribute directly. Where the answer is
    undefined — an `ambiguous` segment, or the terminal snapshot, which no
    segment covers (§5 rule 4) — it proposes nothing and the entry falls back."""
    seg = next((s for s in ctx["segments"]
                if int(s["t_start"]) <= snap["t_us"] < int(s["t_end"])), None)
    attrs = (seg or {}).get("attributes") or {}
    if seg is None or "background_wanted" not in attrs:
        return None, {"segment": seg}
    return ({"system": {"mode": seg["mode"],
                        "background_wanted": bool(attrs["background_wanted"])}},
            {"segment": seg})


def recognize_random(_snap, ctx):
    """`random` draws a row uniformly, from the seed and nothing else: the floor
    a real recognizer has to beat. The rows are sorted before the draw so the
    same seed gives the same sequence on any machine."""
    ordered = ctx["ordered_rows"]
    draw = ctx["rng"].randrange(len(ordered))
    mode, wanted = ordered[draw]
    return ({"system": {"mode": mode, "background_wanted": wanted}},
            {"draw": draw, "row": {"mode": mode, "background_wanted": wanted}})


RECOGNIZERS = {"fixed": recognize_fixed,
               "oracle": recognize_oracle,
               "random": recognize_random}


# ------------------------------------------------------------- the validator

def validate(config):
    """The validator seat (`docs/recognition-vocabulary.md` §2, the five rules),
    run on the composed configuration the simulator will receive — not on the raw
    proposal block. This skeleton only ever sees configurations composed from the
    driver table, so a violation here is a broken table rather than a bad answer,
    and it is raised instead of being clamped: the conditions that can produce a
    `clamped` or `held` entry are the ones not implemented yet.

    Returns the provenance to record, which for a legal configuration is
    `unmodified`."""
    algorithm = config.get("algorithm")
    if algorithm not in ALGORITHMS:
        raise DaemonError(f"driver table composed an unknown algorithm {algorithm!r}")
    violations = check_params(algorithm, config.get("params") or {})
    if violations:
        raise DaemonError(f"{algorithm}: " + "; ".join(violations))
    cap = config.get("batch_bandwidth_cap")
    if cap is not None and not CAP_RANGE[0] <= cap <= CAP_RANGE[1]:
        raise DaemonError(f"batch_bandwidth_cap {cap} outside "
                          f"[{CAP_RANGE[0]}, {CAP_RANGE[1]}]")
    return "unmodified"


# ------------------------------------------------------------------- the run

def run(doc, condition, table, boot, seed=None, telemetry="focus"):
    """(config schedule, recognition log) for one workload under one condition and
    one telemetry shape.

    The schedule's first entry is always the boot default at t = 0 with
    provenance `fallback` (§7); after it, **every query point yields exactly one
    entry**, so the provenance breakdown is computable from the schedule alone.
    These three conditions have no inference to wait for, so an entry is stamped
    at its query point (`latency_us` 0, §8) — which means the t = 0 answer lands
    on the same microsecond as the boot entry and, by the Order rule, after it.
    """
    if telemetry not in TELEMETRY:
        raise DaemonError(f"telemetry shape {telemetry!r}: one of {', '.join(TELEMETRY)}")
    if condition in UNIMPLEMENTED:
        raise DaemonError(f"condition {condition!r} is not implemented in this daemon yet; "
                          f"it implements {', '.join(CONDITIONS)}")
    if condition not in CONDITIONS:
        raise DaemonError(f"condition {condition!r}: unknown")
    if condition in DRAWING and seed is None:
        raise DaemonError(f"condition {condition!r} draws and needs a seed")
    if condition not in DRAWING and seed is not None:
        raise DaemonError(f"condition {condition!r} does not draw; no seed belongs")

    wid = workload_id(doc)
    schedule = {"workload_id": wid, "condition": condition,
                "schedule": [{"t_us": 0, "config": boot, "provenance": "fallback"}]}
    log = {"workload_id": wid, "condition": condition, "seed": seed,
           "telemetry": telemetry, "queries": []}
    if condition == "fixed":
        return schedule, log       # no recognizer, no query points, one entry

    ctx = {"segments": doc.get("ground_truth") or [],
           "ordered_rows": sorted(table),
           "rng": random.Random(seed)}
    recognizer = RECOGNIZERS[condition]
    for snap in snapshots(projection(doc), telemetry):
        proposal, source = recognizer(snap, ctx)
        row = None
        if proposal is not None:
            system = proposal["system"]
            row = table.get((system["mode"], bool(system["background_wanted"])))
        if row is None:            # nothing proposed, or a row the table cannot serve
            proposal, provenance, config = None, "fallback", boot
        else:
            config = compose(row)
            provenance = validate(config)
        log["queries"].append({"t_set_change": snap["t_us"], "telemetry": snap,
                               "proposal": proposal, "validation": provenance,
                               "latency_us": 0, "source": source})
        schedule["schedule"].append({"t_us": snap["t_us"], "config": config,
                                     "provenance": provenance})
    return schedule, log


def write(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1)
        f.write("\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="daemon.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--workload", required=True, help="canonical workload file")
    ap.add_argument("--condition", required=True)
    ap.add_argument("--telemetry", required=True, choices=TELEMETRY)
    ap.add_argument("--driver-table", required=True, dest="driver_table")
    ap.add_argument("--boot-default", required=True, dest="boot_default")
    ap.add_argument("--out-schedule", required=True, dest="out_schedule")
    ap.add_argument("--out-log", required=True, dest="out_log")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args(argv)
    try:
        with open(args.workload, "r", encoding="utf-8") as f:
            doc = json.load(f)
        with open(args.boot_default, "r", encoding="utf-8") as f:
            boot = json.load(f)
        table = read_driver_table(args.driver_table)
        schedule, log = run(doc, args.condition, table, boot,
                            seed=args.seed, telemetry=args.telemetry)
    except (DaemonError, OSError, ValueError, KeyError) as exc:
        print(f"daemon: {exc}", file=sys.stderr)
        return 1
    write(schedule, args.out_schedule)
    write(log, args.out_log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
