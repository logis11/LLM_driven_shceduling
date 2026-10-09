"""timeline + archetypes.yaml -> canonical workload (interpretation-contract §2–§7).

Compile time resolves all randomness; run time resolves all timing that
scheduling can influence. Concretely:

- Bounded per-iteration sequences are unrolled with per-iteration draws
  (input-driven bursts, finite jobs, spawn tables); unbounded (segment-bound)
  loops compile to LOOP-unbounded bodies whose per-iteration params degrade
  to per-task draws (contract §5: per-iteration sampling only when bounded).
- Archetype WAIT operands that name a `<x>_wait` param are *blocked-time*
  waits with no waker task and compile to SLEEP(sampled); WAIT operands
  without one are real channels (input, children, chain wiring).
- The chain constructor (contract §6) expands game-task-chain at compile
  time into chain_length driven members.
- The lane-scaling pass (the one compile mode, `single`) transforms
  declared-scalable fields only — for game-task-chain, chain RUN values are
  scaled so the chain's aggregate demand is lane_share of the lane. The
  unscaled `native` mode left with the native set (9.5 spec decision 14, 9.13).
"""

import bisect
import gzip
import json
import math
import pathlib

from . import sampling
from .estimate import per_segment
from .units import parse_us

MODES = ("single",)


class _TaskBuild:
    def __init__(self, task_id, name, declared_class):
        self.id = task_id
        self.name = name
        self.declared_class = declared_class   # the bound entry's (9.13 spec decision 2)
        self.program = []
        self.spawn_table = None
        self.fork_cap = None
        self.depart = None
        self.replay = None   # 9.14 decision 12: what the trace-replay variant did for this task, if anything
        self.demand_us = 0  # exact static CPU demand, accumulated in-context


def compile_timeline(timeline, library, mode, rel_path=None):
    """Returns (canonical_dict, demand_report)."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    builds, wakes = [], []
    for task in timeline.tasks:
        instance_ids = ([task["id"]] if task["count"] == 1 else
                        [f"{task['id']}.{n}" for n in range(1, task["count"] + 1)])
        for iid in instance_ids:
            builds.extend(_compile_instance(timeline, library, task, iid,
                                            mode, wakes))

    events = [_arrive_event(b) for b in builds]
    events += [{"t": t, "op": "wake", "target": target, "channel": channel}
               for (t, target, channel) in wakes]
    events.sort(key=lambda e: (e["t"], e["op"],
                               e.get("id", e.get("target", ""))))

    rel = rel_path or timeline.path.name
    canonical = {
        "meta": {
            "id": timeline.id,
            "derived_from": f"{rel}@{timeline.blob_hex}",
            "sampled": {"seed": timeline.seed,
                        "archetypes": f"archetypes.yaml@{library.blob_hex}"},
        },
        "ground_truth": [_ground_truth_segment(s) for s in timeline.segments],
        "events": events,
    }
    duration = timeline.duration_us
    per_task = {b.id: b.demand_us for b in builds}
    report = {
        "duration_us": duration,
        "demand_us": sum(per_task.values()),
        "utilization": sum(per_task.values()) / duration,
        "per_task": per_task,
        "per_segment": per_segment(builds, timeline.segments, duration),   # 9.14 decision 4
        "operations": {b.id: b.operations for b in builds if getattr(b, "operations", None)},
        "demand_class": timeline.demand_class,
    }
    replay = {b.id: b.replay for b in builds if b.replay}
    if replay:   # 9.14 decision 12: the trace-replay variant's provenance per task
        report["replay"] = replay
    return canonical, report


def canonical_bytes(canonical):
    """The byte form the manifest hashes and the invariants diff."""
    return (json.dumps(canonical, sort_keys=True, separators=(",", ":"))
            + "\n").encode()


def _ground_truth_segment(segment):
    """A labeled interval. `familiarity` is carried only when the timeline
    authored it — never null, never derived — so the grader's split key is
    exactly what the author declared."""
    entry = {"t_start": segment["t_start"], "t_end": segment["t_end"],
             "mode": segment["mode"], "attributes": segment["attributes"]}
    if segment.get("familiarity") is not None:
        entry["familiarity"] = segment["familiarity"]
    return entry


def _arrive_event(build):
    event = {"t": build.arrive, "op": "arrive", "id": build.id,
             "name": build.name, "declared_class": build.declared_class,
             "program": build.program}
    if build.depart is not None:
        event["depart"] = build.depart
    if build.spawn_table is not None:
        event["spawn_table"] = build.spawn_table
        event["fork_cap"] = build.fork_cap
    return event


# ---- per-instance synthesis -------------------------------------------------

def _compile_instance(timeline, library, task, iid, mode, wakes):
    entry = library.entry(task["archetype"])
    if entry["pattern"].get("constructor") == "chain":
        return _chain_constructor(timeline, task, iid, entry, mode)

    build = _TaskBuild(iid, task["name"], entry["declared_class"])
    build.arrive = task["arrive"]
    build.depart = task["depart"]
    lifespan = (task["depart"] or timeline.duration_us) - task["arrive"]
    seed = timeline.seed
    params = entry.get("params") or {}
    program = entry["pattern"]["program"]

    if entry["pattern"].get("constructor") == "module-build":
        _module_build_unroll(build, library, task, iid, seed, params, entry)
    elif library.is_measured(task["archetype"]):
        _measured_unroll(build, timeline, task, iid, params, wakes)
    elif library.has_input_channel(task["archetype"]):
        _interactive_unroll(build, timeline, task, iid, params, wakes)
    elif _is_fork_loop(program):
        _orchestrator_unroll(build, library, task, iid, seed, params, program)
    elif entry["pattern"].get("constructor") == "batch-loop":
        _batch_loop(build, params, task, seed, iid)
    elif entry["lifetime"] == "finite":
        _finite_unroll(build, task, iid, seed, params, program)
    else:
        _unbounded_loop(build, iid, seed, params, program, lifespan)
    return [build]


def _is_fork_loop(program):
    return any("FORK" in step
               for step in _flatten(program))


def _flatten(program):
    for step in program:
        (op, operand), = step.items()
        if op == "loop":
            yield from _flatten(operand)
        else:
            yield step


def _resolve_wait(operand, params, iid):
    """`WAIT: x` -> SLEEP param name if `x_wait` exists, else a channel."""
    if f"{operand}_wait" in params:
        return ("sleep-param", f"{operand}_wait")
    return ("channel", f"{operand}:{iid}")


def _draw(params, name, seed, iid, k):
    param = params[name]
    index = 0 if param.get("sampling") == "per-task" else k
    return sampling.sample(param, seed, iid, name, index)


# ---- segment-bound unbounded loops (entries without measured components) --

def _unbounded_loop(build, iid, seed, params, program, lifespan):
    body, cycle_run, cycle_wall, period = [], 0, 0, None
    steps = list(_flatten(program))
    for step in steps:
        (op, operand), = step.items()
        if op == "RUN":
            us = _draw(params, operand, seed, iid, 0)
            body.append({"op": "RUN", "us": us})
            cycle_run += us
            cycle_wall += us
        elif op == "SLEEP":
            us = _draw(params, operand, seed, iid, 0)
            body.append({"op": "SLEEP", "us": us})
            cycle_wall += us
        elif op == "TIMER":
            period = _draw(params, operand, seed, iid, 0)
            body.append({"op": "TIMER", "period_us": period})
        elif op == "WAIT":
            kind, value = _resolve_wait(operand, params, iid)
            if kind == "sleep-param":
                us = _draw(params, value, seed, iid, 0)
                body.append({"op": "SLEEP", "us": us})
                cycle_wall += us
            else:
                body.append({"op": "WAIT", "channel": value})
        else:
            raise ValueError(f"unexpected op {op!r} in unbounded loop of {iid}")
    build.program = [{"op": "LOOP", "count": "unbounded", "body": body}]
    cycle = period if period is not None else max(cycle_wall, 1)
    build.demand_us = round(cycle_run / cycle * lifespan)


# ---- measured archetypes (9.5 fold-in: D9, D13, D16, D17, D18) ----------------
#
# One task, one explicit time-ordered event stream over its lifetime:
#   - timer components (`components`): each comm's wakes are sampled from its
#     measured gap quantiles over the whole lifetime, each wake's RUN from its
#     run quantiles; cadence archetypes (`focus_components`) swap to the
#     driven-phase components inside focus windows; every component starts as
#     a stream already running — at arrival, and at each focus window's or
#     operation's start (9.5 D77);
#   - replayed stimulus (`stimulus`): inside each focus window a contiguous
#     slice of the named stream (dataset/stimulus/<stream>.jsonl) of the
#     window's length, at an offset drawn from the seed; each input is an
#     exogenous wake on the task's input channel with a RUN from `input_run`.
# Timer wakes compile to WAIT steps on the task's timer channel, each woken by a
# `wake` event at its sampled absolute time, with no deadline (9.5 D74); input
# wakes to WAIT steps on the input channel plus `wake` events, as before.
# A periodic archetype (`period`, `cycle_run`: the playback and call entries,
# 9.5 D75) compiles to one TIMER step per medium cycle over the lifetime, each
# followed by its cycle's run — TIMER carries a period with a deadline only.

_STREAMS = {}


def _load_stream(name, kinds=None):
    """The stream's event times, or only those of the named kinds — the events the measurement replayed (9.5 D28,
    D65: `office-writer` and `web-browser` were measured with the keys alone)."""
    key = (name, tuple(kinds) if kinds else None)
    if key not in _STREAMS:
        path = pathlib.Path(__file__).resolve().parents[2] / "stimulus" / f"{name}.jsonl"
        events = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        _STREAMS[key] = [e["t_us"] for e in events if not kinds or e.get("kind") in kinds]
    return _STREAMS[key]


def _heavy_events(heavy, seed, iid, t0, t1):
    """9.5 D64's heavy events, each at its carried rate at no fixed time: intervals drawn exponential (the
    measurement saw at most one per session, so no interval was measured and none is carried), each run from the
    event's measured run table."""
    events = []
    for index, ev in enumerate(heavy or []):
        rate = ev["rate_per_s"]
        if not rate:
            continue
        t, k = t0, 0
        while True:
            u = sampling.uniform(seed, iid, "heavy", index, k, "gap")
            t += max(1, round(-math.log(u) / rate * 1e6))
            if t >= t1:
                break
            events.append((t, sampling.sample(ev["run"], seed, iid, "heavy", index, k, "run"), "timer"))
            k += 1
    return events


def _component_events(components, seed, iid, t0, t1, tag):
    """9.5 D77: each component over [t0, t1) — a task's lifetime, a focus window, an operation — is a stream already
    running at t0: its first wake falls one forward-recurrence gap after t0, then gap after gap from its table."""
    events = []
    for index, comp in enumerate(components):
        key = (tag, index, comp["comm"])
        t, k = t0 + sampling.sample_first_gap(comp["gap"], seed, iid, *key), 0
        while t < t1:
            run = sampling.sample(comp["run"], seed, iid, *key, k, "run")
            events.append((t, run, "timer"))
            k += 1
            t += sampling.sample(comp["gap"], seed, iid, *key, k, "gap")
    return events


def _periodic_unroll(build, seed, iid, params, t0, t1, launch=None, replay=None):
    """9.5 D75: one job per medium cycle — TIMER(period) at arrival + k·period over the lifetime (contract §3's absolute
    grid, tick 0 consumed at arrival), each followed by its cycle's run drawn from the measured per-cycle table. A launch
    phase (9.10 D138) is binned onto the grid: a cycle starting inside it runs the replay's CPU in its window. Under a
    trace replay (9.14 decision 12) the grid and the period stay and the k-th tick takes the k-th observed cycle's work
    from the window's offset, in order; a stream holding too few cycles fails the build."""
    period = sampling.sample(params["period"], seed, iid, "period", 0)
    phase_us, binned = 0, {}
    if launch:
        phase_us = launch[0]
        for t_rel, run in launch[1]:
            if t_rel < phase_us:
                binned[t_rel // period] = binned.get(t_rel // period, 0) + run
    works = None
    if replay:
        works = [work for t_rel, work, _ in replay["stream"] if t_rel >= replay["offset"]]
        ticks = -(-(t1 - t0) // period)
        if len(works) < ticks:
            raise ValueError(f"{iid}: {replay['archetype']}'s replay stream {replay['name']!r} holds {len(works)} "
                             f"cycles from its offset, short of the task's {ticks} ticks")
    t, k = t0, 0
    while t < t1:
        build.program.append({"op": "TIMER", "period_us": period})
        if works is not None:
            run = works[k]
        elif t - t0 < phase_us:
            run = binned.get(k, 0)
        else:
            run = sampling.sample(params["cycle_run"], seed, iid, "cycle", k, allow_zero=True)
        if run:
            build.program.append({"op": "RUN", "us": run})
            build.demand_us += run
        t += period
        k += 1


def _measured_unroll(build, timeline, task, iid, params, wakes):
    seed = timeline.seed
    channel = f"input:{iid}"
    timer_channel = f"timer:{iid}"
    t0 = task["arrive"]
    t1 = task["depart"] or timeline.duration_us
    # 9.14 decision 12: under a trace replay the observed stream stands in for the components, the heavy events and
    # the launch phase alike; the operations and the stimulus stay as compiled
    replay = _replay_window(task, iid, seed, params, "cycles" if "cycle_run" in params else "wakes", t0, t1)
    launch = None if replay else _launch_stream(task, iid, seed, params)
    if replay:
        build.replay = {"stream": replay["name"], "offset_us": replay["offset"]}
    if "cycle_run" in params:
        _periodic_unroll(build, seed, iid, params, t0, t1, launch, replay)
        return
    t_steady = t0 + launch[0] if launch else t0   # D136: the steady stream begins at the launch phase's end
    windows = [w for w in timeline.focus if w["task"] == task["id"]]
    # operations (spec decisions 8–9): a window from the authored start for a duration drawn from the measured
    # table; inside it the operation's components replace whatever is active and no input wake is emitted
    op_windows = []
    for j, op in enumerate(o for o in timeline.operations if o["task"] == task["id"]):
        spec = params["operations"][op["name"]]
        dur = sampling.sample(spec["duration"], seed, iid, "operation", j)
        op_windows.append({"from": op["at"], "to": min(op["at"] + dur, t1), "name": op["name"], "spec": spec})
    build.operations = [{"name": w["name"], "at_us": w["from"], "duration_us": w["to"] - w["from"]} for w in op_windows]

    def in_operation(t):
        return any(w["from"] <= t < w["to"] for w in op_windows)
    events = []
    focus_components = params.get("focus_components")
    if replay:
        # the observed wakes from the window's offset, each a timer wake at its time from the arrival; an operation's
        # window replaces them as it replaces the components (D137)
        for t_rel, run, _ in replay["stream"]:
            if t_rel < replay["offset"]:
                continue
            t = t0 + (t_rel - replay["offset"])
            if t >= t1:
                break
            if not in_operation(t):
                events.append((t, run, "timer"))
    else:
        # the launch phase's replay (9.10 D136): each observed wake a timer wake at its time from the arrival; an
        # operation's window replaces it as it replaces the components (D137)
        if launch:
            for t_rel, run in launch[1]:
                t = t0 + t_rel
                if t_rel >= launch[0] or t >= t1:
                    break
                if not in_operation(t):
                    events.append((t, run, "timer"))
        # timer components over the lifetime past any launch phase; cadence archetypes swap inside focus windows
        for ev in _component_events(params.get("components") or [], seed, iid, t_steady, t1, "idle"):
            if focus_components and any(w["from"] <= ev[0] < w["to"] for w in windows):
                continue
            if in_operation(ev[0]):
                continue
            events.append(ev)
        events.extend(ev for ev in _heavy_events(params.get("heavy_events"), seed, iid, t_steady, t1)
                      if not in_operation(ev[0]))
        if focus_components:
            for j, w in enumerate(windows):
                events.extend(ev for ev in _component_events(focus_components, seed, iid, w["from"], w["to"], ("focus", j))
                              if not in_operation(ev[0]))
    for j, w in enumerate(op_windows):
        events.extend(_component_events(w["spec"]["components"], seed, iid, w["from"], w["to"], ("operation", j)))
    # replayed stimulus inside focus windows
    stimulus = params.get("stimulus")
    if stimulus:
        stream = _load_stream(stimulus["stream"], stimulus.get("kinds"))
        span = stream[-1] if stream else 0
        k = 0
        for j, w in enumerate(windows):
            length = w["to"] - w["from"]
            offset = round(sampling.uniform(seed, iid, "stimulus", j) * max(0, span - length))
            lo = bisect.bisect_left(stream, offset)
            for t_rel in stream[lo:]:
                if t_rel >= offset + length:
                    break
                t = w["from"] + (t_rel - offset)
                if in_operation(t):
                    continue
                run = sampling.sample(params["input_run"], seed, iid, "input", k, allow_zero=True)
                events.append((t, run, "input"))
                k += 1
    events.sort(key=lambda e: (e[0], e[2] != "timer"))
    for t, run, kind in events:
        wake_channel = timer_channel if kind == "timer" else channel   # D74: a timer wake carries no deadline
        wakes.append((t, iid, wake_channel))
        build.program.append({"op": "WAIT", "channel": wake_channel})
        if run:   # a zero input_run is measured, not missing: the input woke the task and cost no CPU (D48)
            build.program.append({"op": "RUN", "us": run})
            build.demand_us += run
    if not build.program:  # alive but silent: block forever
        build.program = [{"op": "WAIT", "channel": channel}]


# ---- launch phases (9.10 D21, D133, D136–D138) -------------------------------
#
# An entry with a `launch` param carries its observed launch phase (dataset/launch/<stream>.json.gz): per pooled
# repeat, the phase's length and one or more streams of wakes, each [t_us from the phase's start, run_us, thread].
# A task the file starts mid-file — arriving after 0 s; one at 0 s is already steady (D21) — draws one repeat by the
# file's seed; a task group (`count`) draws one repeat and distinct streams of it, the four hidden tabs' renderers of
# one launch (D133).

_LAUNCH = {}


def _load_launch(name):
    if name not in _LAUNCH:
        path = pathlib.Path(__file__).resolve().parents[2] / "launch" / f"{name}.json.gz"
        with gzip.open(path, "rt") as handle:
            _LAUNCH[name] = json.load(handle)
    return _LAUNCH[name]


def _launch_stream(task, iid, seed, params):
    """(phase length µs, [(t_rel_us, run_us), …] sorted) for this instance; None without a launch phase."""
    spec = params.get("launch")
    if not spec or task["arrive"] <= 0:
        return None
    reps = _load_launch(spec["stream"])["repeats"]
    rep = reps[min(int(sampling.uniform(seed, task["id"], "launch", "repeat") * len(reps)), len(reps) - 1)]
    streams = rep["streams"]
    order = sorted(range(len(streams)), key=lambda i: sampling.uniform(seed, task["id"], "launch", "stream", i))
    n = int(iid.rsplit(".", 1)[1]) - 1 if task["count"] > 1 else 0
    if n >= len(order):
        raise ValueError(f"{iid}: {task['count']} tasks draw from a launch repeat of {len(order)} streams")
    return rep["phase_us"], [(w[0], w[1]) for w in streams[order[n]]]


# ---- trace replay (9.14 decision 12; dataset/variants.yaml's `replay` set) ---------
#
# An entry whose params carry `replay: {stream, sampling: per-task, source}` compiles each of its tasks from one pooled
# repeat's observed stream, dataset/replay/<stream>.json.gz, written by dataset/tools/meas/replay_fold_in.py from the
# raw release: {entry, program, kind, source, …, repeats: [{repeat, run_id, phase_us, comms, streams}]}, one repeat, one
# or more streams of [t_us, x, y] rows whose columns the `kind` fixes — `wakes` (a measured entry): [t from the phase's
# start, run_us, thread]; `cycles` (a periodic entry): [the cycle's start, its work_us, its length_us]; `runs` (a batch
# entry): [the run's start, run_us, the block_us after it]. A measured or periodic task takes a seeded window of the
# stream — a uniform offset by the file's seed over the phase's span less the task's lifetime, as the stimulus replay
# draws its window — and a task group (`count`) distinct streams of the repeat, as the launch phases are drawn; a
# batch task takes the job's runs from its start. A stream shorter than its task fails the build; nothing is wrapped
# or padded. A batch stream naming a program applies to tasks bound to it alone.

_REPLAY = {}


def _load_replay(name):
    if name not in _REPLAY:
        path = pathlib.Path(__file__).resolve().parents[2] / "replay" / f"{name}.json.gz"
        with gzip.open(path, "rt") as handle:
            _REPLAY[name] = json.load(handle)
    return _REPLAY[name]


def _replay_window(task, iid, seed, params, kind, t0, t1):
    """{name, archetype, offset, stream, doc} for this instance's replay, or None without a `replay` param."""
    spec = params.get("replay")
    if not spec:
        return None
    name, archetype = spec["stream"], task["archetype"]
    doc = _load_replay(name)
    if doc.get("kind") != kind:
        raise ValueError(f"{iid}: {archetype} needs a {kind} replay stream; {name!r} holds {doc.get('kind')}")
    rep = doc["repeats"][0]
    streams = rep["streams"]
    order = sorted(range(len(streams)), key=lambda i: sampling.uniform(seed, task["id"], "replay", "stream", i))
    n = int(iid.rsplit(".", 1)[1]) - 1 if task["count"] > 1 else 0
    if n >= len(order):
        raise ValueError(f"{iid}: {task['count']} tasks draw from a replay repeat of {len(order)} streams")
    stream = sorted(streams[order[n]])
    offset = 0
    if kind != "runs":
        span, length = rep["phase_us"], t1 - t0
        if span < length:
            raise ValueError(f"{iid}: {archetype}'s replay stream {name!r} spans {span} µs, shorter than the "
                             f"task's {length} µs")
        offset = round(sampling.uniform(seed, iid, "replay", "offset") * (span - length))
    return {"name": name, "archetype": archetype, "offset": offset, "stream": stream, "doc": doc}


def _replay_batch_ops(replay, total, iid):
    """The batch loop's ops from the observed runs and the block after each, in time order, until `total` µs of CPU
    are spent; a zero block joins the runs on either side into one RUN, as _batch_ops does."""
    pairs = [(run, block) for _t, run, block in replay["stream"]]
    held = sum(run for run, _ in pairs)
    if held < total:
        raise ValueError(f"{iid}: {replay['archetype']}'s replay stream {replay['name']!r} holds {held} µs of CPU, "
                         f"short of the bind's {total} µs")
    spent, ops, pending = 0, [], 0
    for run, block in pairs:
        if spent >= total:
            break
        us = min(max(1, int(run)), total - spent)
        pending += us
        spent += us
        block = int(block)
        if block >= 1 and spent < total:
            ops.append({"op": "RUN", "us": pending})
            ops.append({"op": "SLEEP", "us": block})
            pending = 0
    if pending:
        ops.append({"op": "RUN", "us": pending})
    return ops


# ---- input-driven tasks (desktop-interactive) -------------------------------

def _interactive_unroll(build, timeline, task, iid, params, wakes):
    seed = timeline.seed
    channel = f"input:{iid}"
    k = 0
    for window in timeline.focus:
        if window["task"] != task["id"]:
            continue
        t = window["from"]
        while True:
            gap = _draw(params, "input_gap", seed, iid, k)
            t += gap
            if t >= window["to"]:
                break
            fraction = _draw(params, "burst_fraction", seed, iid, k)
            burst = max(1, round(fraction * gap))
            wakes.append((t, iid, channel))
            build.program.append({"op": "WAIT", "channel": channel})
            build.program.append({"op": "RUN", "us": burst})
            build.demand_us += burst
            k += 1
    if not build.program:  # alive but never focused: block forever
        build.program = [{"op": "WAIT", "channel": channel}]


# ---- finite jobs (cpu-batch and the one-table-set batch loops: file-archiver, game-download, incremental-backup, …) ----

def _batch_loop(build, params, task, seed, iid):
    """cpu-batch (D21, D22, D25): a RUN drawn from the bound program's measured runs between voluntary blocks,
    then the program's off-CPU time that followed such a run — the block table is zero-inclusive, a zero meaning
    another thread of the program ran on — until `total_work` of CPU is spent. The table set is chosen by the
    `program` binding, never by the task's display name. An archetype with one table set (9.7 D29: `file-archiver`,
    `game-download`; 9.10's measured jobs, `incremental-backup` among them) needs no `program` binding: its one set is
    taken."""
    program = task["bind"].get("program")
    if program is None:
        sets = sorted(name[:-len("_run")] for name in params if name.endswith("_run"))
        if len(sets) != 1:
            raise ValueError(f"{iid}: a batch loop with {len(sets)} table sets needs a `program` binding")
        program = sets[0]
    total = parse_us(task["bind"]["total_work"])
    if program == "spoof":   # the chrome spoof is one uninterrupted RUN by construction (D7)
        build.program = [{"op": "RUN", "us": total}, {"op": "EXIT"}]
        build.demand_us = total
        return
    replay = _replay_window(task, iid, seed, params, "runs", 0, 0)   # 9.14 decision 12: the job's observed runs
    if replay and replay["doc"].get("program") not in (None, program):
        build.replay = {"stream": replay["name"], "applied": False, "program": program}
        replay = None
    if replay:
        build.replay = {"stream": replay["name"], "offset_us": 0}
        ops = _replay_batch_ops(replay, total, iid)
    else:
        ops = _batch_ops(params[f"{program}_run"], params[f"{program}_block"], total, seed, iid, "batch")
    ops.append({"op": "EXIT"})
    build.program, build.demand_us = ops, total


def _batch_ops(runs, blocks, total, seed, iid, tag):
    """The batch loop's ops (D21, D22, D25): runs drawn from `runs` and, after each, a block drawn from `blocks`,
    until `total` µs of CPU are spent; a zero block joins the runs on either side into one RUN."""
    spent, k, ops, pending = 0, 0, [], 0
    while spent < total:
        us = min(max(1, int(sampling.sample(runs, seed, iid, f"{tag}_run", str(k)))), total - spent)
        pending += us
        spent += us
        block = int(sampling.sample(blocks, seed, iid, f"{tag}_block", str(k), allow_zero=True))
        if block >= 1 and spent < total:
            ops.append({"op": "RUN", "us": pending})   # a zero block means the program ran on (D25): the runs it
            ops.append({"op": "SLEEP", "us": block})   # separates join one RUN, the same CPU between two blocks
            pending = 0
        k += 1
    if pending:
        ops.append({"op": "RUN", "us": pending})
    return ops


def _finite_unroll(build, task, iid, seed, params, program):
    total_work = parse_us(task["bind"]["total_work"])
    steps = list(_flatten(program))
    has_loop = any("loop" in step for step in program)
    if not has_loop:  # cpu-batch shape: RUN(total_work); EXIT
        build.program = [{"op": "RUN", "us": total_work}, {"op": "EXIT"}]
        build.demand_us = total_work
        return
    k, done = 0, 0
    while done < total_work:
        for step in steps:
            (op, operand), = step.items()
            if op == "EXIT":
                continue
            if op == "RUN":
                us = _draw(params, operand, seed, iid, k)
                build.program.append({"op": "RUN", "us": us})
                done += us
            elif op == "WAIT":
                kind, value = _resolve_wait(operand, params, iid)
                if kind == "sleep-param":
                    us = _draw(params, value, seed, iid, k)
                    build.program.append({"op": "SLEEP", "us": us})
                else:
                    build.program.append({"op": "WAIT", "channel": value})
            else:
                raise ValueError(f"unexpected op {op!r} in finite loop of {iid}")
        k += 1
    build.program.append({"op": "EXIT"})
    build.demand_us = done


# ---- orchestrators (build-orchestrator) -------------------------------------

# D19, D20: one make job as six member processes — the roles in fork order, each with its structural step count
OBJECT_JOB = (("sh", 4), ("gcc", 3), ("cc1", 1), ("as", 1), ("fixdep", 1), ("rm", 1))


def _object_job(parent_iid, job_index, child_entry, seed, child_name):
    """One object job as six spawn-table entries (D19): `sh` runs first, every other member waits on its own
    channel and is woken in the job's parent-child order (D2) — sh, gcc, cc1, gcc, as, gcc, sh, fixdep, sh, rm, sh
    — each member's step CPU drawn from its own (role, step) table (D20). A member that has finished waits,
    without CPU, until `sh` ends the job, so `fork_cap` bounds the jobs in flight, as make's jobserver counts them.
    Returns (spawn-table entries in fork order, their CPU)."""
    params = child_entry["params"]
    ids = {role: f"{parent_iid}.j{job_index + 1}.{role}" for role, _ in OBJECT_JOB}
    names = {role: role for role, _ in OBJECT_JOB} | {"cc1": child_name}
    demand = 0

    def run(role, step):
        nonlocal demand
        us = int(sampling.sample(params[f"{role}_step_{step}"], seed, parent_iid,
                                 "job", str(job_index), role, str(step)))
        demand += us
        return {"op": "RUN", "us": us}

    def wait(role):
        return {"op": "WAIT", "channel": f"job:{ids[role]}"}

    def wake(role):
        return {"op": "WAKE", "target": ids[role]}

    bodies = {
        "sh": [run("sh", 1), wake("gcc"), wait("sh"), run("sh", 2), wake("fixdep"), wait("sh"),
               run("sh", 3), wake("rm"), wait("sh"), run("sh", 4)]
              + [wake(r) for r, _ in OBJECT_JOB if r != "sh"] + [{"op": "EXIT"}],
        "gcc": [wait("gcc"), run("gcc", 1), wake("cc1"), wait("gcc"), run("gcc", 2), wake("as"),
                wait("gcc"), run("gcc", 3), wake("sh"), wait("gcc"), {"op": "EXIT"}],
        "cc1": [wait("cc1"), run("cc1", 1), wake("gcc"), wait("cc1"), {"op": "EXIT"}],
        "as": [wait("as"), run("as", 1), wake("gcc"), wait("as"), {"op": "EXIT"}],
        "fixdep": [wait("fixdep"), run("fixdep", 1), wake("sh"), wait("fixdep"), {"op": "EXIT"}],
        "rm": [wait("rm"), run("rm", 1), wake("sh"), wait("rm"), {"op": "EXIT"}],
    }
    return [{"id": ids[role], "name": names[role], "declared_class": child_entry["declared_class"],
             "program": bodies[role]}
            for role, _ in OBJECT_JOB], demand


def _orchestrator_unroll(build, library, task, iid, seed, params, program):
    spawn_count = int(task["bind"]["spawn_count"])
    build.fork_cap = int(task["bind"]["parallelism_cap"]) * len(OBJECT_JOB)   # D19: jobs in flight, six members each
    child_entry = library.entry(library.entry(task["archetype"])["spawns"])
    child_name = task["bind"].get("child_name", "cc1")

    build.spawn_table = []
    for i in range(spawn_count):
        entries, demand = _object_job(iid, i, child_entry, seed, child_name)
        build.spawn_table.extend(entries)
        build.demand_us += demand

    for i in range(spawn_count):   # one dispatch run per job, then its six members are forked together (D19)
        us = _draw(params, "dispatch_overhead", seed, iid, i)
        build.program.append({"op": "RUN", "us": us})
        build.program.extend({"op": "FORK"} for _ in OBJECT_JOB)
        build.demand_us += us
    build.program.append({"op": "WAIT", "channel": f"children:{iid}"})
    build.program.append({"op": "EXIT"})


# ---- the DKMS module build (module-build-orchestrator, 9.10 D52–D57) ---------------------------

def _tree_nodes(tree, parent=None):
    """A job tree from the child entry's pattern — a node is a member id, or {member id: [child nodes]} — as
    [(member id, parent id, [child ids])] depth-first, children in fork order."""
    out = []
    for node in tree if isinstance(tree, list) else [tree]:
        if isinstance(node, dict):
            (mid, kids), = node.items()
        else:
            mid, kids = node, []
        names = [next(iter(k)) if isinstance(k, dict) else k for k in kids]
        out.append((mid, parent, names))
        out.extend(_tree_nodes(kids, mid))
    return out


def _tree_job(parent_iid, job_index, kind, tree, params, seed, names, declared_class):
    """One make job of `kind` as spawn-table entries, one per member of its tree (D53), in the object job's form
    (9.6 D19, D20; _object_job): the root runs first; every other member waits on its own channel until its parent
    wakes it; a member with children runs a step, wakes its next child and waits for it, runs its next step, and so
    on; a member wakes its parent when its last step is done and waits, without CPU, until the root ends the job.
    Each step's CPU is drawn from the kind's (member, step) table; each member carries the child entry's
    `declared_class`. Returns (entries in fork order, their CPU)."""
    nodes = _tree_nodes(tree)
    ids = {mid: f"{parent_iid}.j{job_index + 1}.{mid}" for mid, _p, _k in nodes}
    demand = 0

    def run(mid, step):
        nonlocal demand
        us = int(sampling.sample(params[f"{kind}_{mid}_step_{step}"], seed, parent_iid,
                                 "job", str(job_index), kind, mid, str(step)))
        demand += us
        return {"op": "RUN", "us": us}

    entries = []
    for mid, parent, kids in nodes:
        own = {"op": "WAIT", "channel": f"job:{ids[mid]}"}
        body = [] if parent is None else [own]
        body.append(run(mid, 1))
        for i, c in enumerate(kids):
            body += [{"op": "WAKE", "target": ids[c]}, own, run(mid, i + 2)]
        if parent is None:
            body += [{"op": "WAKE", "target": ids[m]} for m, _p, _k in nodes if m != mid]
        else:
            body += [{"op": "WAKE", "target": ids[parent]}, own]
        body.append({"op": "EXIT"})
        entries.append({"id": ids[mid], "name": names.get(mid, mid), "declared_class": declared_class,
                        "program": body})
    return entries, demand


def _job_order(rle):
    """The pattern's `job_order`, run-length coded ("p21 C2 c1 …"), as one kind letter per job."""
    out = []
    for tok in rle.split():
        out.extend(tok[0] * int(tok[1:] or 1))
    return out


def _module_build_unroll(build, library, task, iid, seed, params, entry):
    """module-build-orchestrator (9.10 D52–D57): the jobs of the measured build in the order it ran them (D53), each
    after one dispatch run (9.6 D19), at most `parallelism_cap` × 6 tasks in flight (D57); then, its children done,
    the build's serial tail as its own batch loop until the tail's CPU is spent (D54)."""
    pat = entry["pattern"]
    child = library.entry(entry["spawns"])
    trees, letters = child["pattern"]["trees"], child["pattern"]["letters"]
    names = dict(child["pattern"].get("names") or {})
    names["cc1"] = task["bind"].get("child_name", names.get("cc1", "cc1"))
    build.fork_cap = int(task["bind"]["parallelism_cap"]) * 6   # D57: 9.6 D19's rule, six members a job
    build.spawn_table = []
    for i, letter in enumerate(_job_order(pat["job_order"])):
        kind = letters[letter]
        entries, demand = _tree_job(iid, i, kind, trees[kind], child["params"], seed, names,
                                    child["declared_class"])
        build.spawn_table.extend(entries)
        build.demand_us += demand
        us = _draw(params, "dispatch_overhead", seed, iid, i)
        build.program.append({"op": "RUN", "us": us})
        build.program.extend({"op": "FORK"} for _ in entries)
        build.demand_us += us
    build.program.append({"op": "WAIT", "channel": f"children:{iid}"})
    tail = int(sampling.sample(params["tail_work"], seed, iid, "tail_work", 0))
    build.program += _batch_ops(params["tail_run"], params["tail_block"], tail, seed, iid, "tail")
    build.program.append({"op": "EXIT"})
    build.demand_us += tail


def _spawned_program(child, entry, seed, parent_iid, index):
    params = entry.get("params") or {}
    for step in _flatten(entry["pattern"]["program"]):
        (op, operand), = step.items()
        if op == "RUN":
            us = sampling.sample(params[operand], seed,
                                 parent_iid, "spawn", index, operand)
            child.program.append({"op": "RUN", "us": us})
            child.demand_us += us
        elif op == "WAIT":
            kind, value = _resolve_wait(operand, params, child.id)
            if kind == "sleep-param":
                us = sampling.sample(params[value], seed,
                                     parent_iid, "spawn", index, value)
                child.program.append({"op": "SLEEP", "us": us})
            else:
                child.program.append({"op": "WAIT", "channel": value})
        elif op == "EXIT":
            child.program.append({"op": "EXIT"})
        else:
            raise ValueError(f"unexpected op {op!r} in spawned program")


# ---- chain constructor (game-task-chain, contract §6) -----------------------

def _chain_constructor(timeline, task, iid, entry, mode):
    seed = timeline.seed
    params = entry["params"]
    lifespan = task["depart"] - task["arrive"]
    chain_len = int(sampling.sample(params["chain_length"], seed, iid,
                                    "chain_length", 0))
    frame = sampling.sample(params["frame_period"], seed, iid, "frame_period", 0)

    # Members in wake order: the game head, then wineserver (the source's
    # coordination hop, fixed RUN), then the remaining game-specific members.
    # The relay stands in for the request/reply round trip the source draws
    # (archetypes.yaml modeling_notes).
    member_ids = [f"{iid}.chain.1", f"{iid}.wineserver"] + \
        [f"{iid}.chain.{k + 1}" for k in range(1, chain_len)]
    # the members after the head and wineserver are named in the timeline (9.10 D26: the names the
    # chain's source shows for the game's threads; an archetype fixes no process name)
    member_names = list(task["bind"]["member_names"])
    if len(member_names) != chain_len - 1:
        raise ValueError(f"{iid}: member_names holds {len(member_names)} names for {chain_len - 1} members")
    names = [task["name"], "wineserver"] + member_names
    runs = [sampling.sample(params["per_schedule_run"], seed, iid,
                            "per_schedule_run", 0),
            sampling.sample(params["wineserver_run"], seed, iid,
                            "wineserver_run", 0)] + \
        [sampling.sample(params["per_schedule_run"], seed, iid,
                         "per_schedule_run", k)  # per-task: keyed by member
         for k in range(1, chain_len)]
    if mode == "single":  # the declared-scalable pass: chain demand -> lane_share
        lane_share = float(task["bind"]["lane_share"])
        factor = lane_share * frame / sum(runs)
        runs = [max(1, round(r * factor)) for r in runs]

    builds = []
    for k, member_id in enumerate(member_ids):
        member = _TaskBuild(member_id, names[k], entry["declared_class"])
        member.arrive, member.depart = task["arrive"], task["depart"]
        body = ([{"op": "TIMER", "period_us": frame}] if k == 0 else
                [{"op": "WAIT", "channel": f"chain:{member_id}"}])
        body.append({"op": "RUN", "us": runs[k]})
        if k + 1 < len(member_ids):
            body.append({"op": "WAKE", "target": member_ids[k + 1]})
        member.program = [{"op": "LOOP", "count": "unbounded", "body": body}]
        member.demand_us = round(runs[k] / frame * lifespan)
        builds.append(member)

    return builds
