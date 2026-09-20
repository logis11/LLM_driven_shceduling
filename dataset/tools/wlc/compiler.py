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
- The lane-scaling pass (`single` mode) transforms declared-scalable fields
  only — for game-task-chain, chain RUN values are scaled so the chain's
  aggregate demand is lane_share of the lane; nothing else differs from
  `native` output.
"""

import bisect
import json
import pathlib

from . import sampling
from .units import parse_us

MODES = ("native", "single")


class _TaskBuild:
    def __init__(self, task_id, name):
        self.id = task_id
        self.name = name
        self.program = []
        self.spawn_table = None
        self.fork_cap = None
        self.depart = None
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
        "operations": {b.id: b.operations for b in builds if getattr(b, "operations", None)},
        "demand_class": timeline.demand_class,
    }
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
             "name": build.name, "program": build.program}
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

    build = _TaskBuild(iid, task["name"])
    build.arrive = task["arrive"]
    build.depart = task["depart"]
    lifespan = (task["depart"] or timeline.duration_us) - task["arrive"]
    seed = timeline.seed
    params = entry.get("params") or {}
    program = entry["pattern"]["program"]

    if library.is_measured(task["archetype"]):
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


# ---- segment-bound unbounded loops (audio, video, electron, daemons) --------

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
#     driven-phase components inside focus windows;
#   - replayed stimulus (`stimulus`): inside each focus window a contiguous
#     slice of the named stream (dataset/stimulus/<stream>.jsonl) of the
#     window's length, at an offset drawn from the seed; each input is an
#     exogenous wake on the task's input channel with a RUN from `input_run`.
# Timer wakes compile to TIMER steps whose periods chain from the previous
# timer deadline (drift-free absolute times, contract §3); input wakes to
# WAIT steps plus `wake` events, as before.

_STREAMS = {}


def _load_stream(name):
    if name not in _STREAMS:
        path = pathlib.Path(__file__).resolve().parents[2] / "stimulus" / f"{name}.jsonl"
        times = [json.loads(line)["t_us"] for line in path.read_text().splitlines() if line.strip()]
        _STREAMS[name] = times
    return _STREAMS[name]


def _component_events(components, seed, iid, t0, t1, tag):
    events = []
    for index, comp in enumerate(components):
        key = (tag, index, comp["comm"])
        t, k = t0, 0
        while True:
            t += sampling.sample(comp["gap"], seed, iid, *key, k, "gap")
            if t >= t1:
                break
            run = sampling.sample(comp["run"], seed, iid, *key, k, "run")
            events.append((t, run, "timer"))
            k += 1
    return events


def _measured_unroll(build, timeline, task, iid, params, wakes):
    seed = timeline.seed
    channel = f"input:{iid}"
    t0 = task["arrive"]
    t1 = task["depart"] or timeline.duration_us
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
    # timer components over the lifetime; cadence archetypes swap inside focus windows
    focus_components = params.get("focus_components")
    for ev in _component_events(params.get("components") or [], seed, iid, t0, t1, "idle"):
        if focus_components and any(w["from"] <= ev[0] < w["to"] for w in windows):
            continue
        if in_operation(ev[0]):
            continue
        events.append(ev)
    if focus_components:
        for j, w in enumerate(windows):
            events.extend(ev for ev in _component_events(focus_components, seed, iid, w["from"], w["to"], ("focus", j))
                          if not in_operation(ev[0]))
    for j, w in enumerate(op_windows):
        events.extend(_component_events(w["spec"]["components"], seed, iid, w["from"], w["to"], ("operation", j)))
    # replayed stimulus inside focus windows
    stimulus = params.get("stimulus")
    if stimulus:
        stream = _load_stream(stimulus["stream"])
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
    last_deadline = t0
    for t, run, kind in events:
        if kind == "timer":
            period = max(1, t - last_deadline)
            last_deadline += period
            build.program.append({"op": "TIMER", "period_us": period})
        else:
            wakes.append((t, iid, channel))
            build.program.append({"op": "WAIT", "channel": channel})
        if run:   # a zero input_run is measured, not missing: the input woke the task and cost no CPU (D48)
            build.program.append({"op": "RUN", "us": run})
            build.demand_us += run
    if not build.program:  # alive but silent: block forever
        build.program = [{"op": "WAIT", "channel": channel}]


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


# ---- finite jobs (cpu-batch, io-stream, network-bulk) -----------------------

def _batch_loop(build, params, task, seed, iid):
    """cpu-batch (D21, D22, D25): a RUN drawn from the bound program's measured runs between voluntary blocks,
    then the program's off-CPU time that followed such a run — the block table is zero-inclusive, a zero meaning
    another thread of the program ran on — until `total_work` of CPU is spent. The table set is chosen by the
    `program` binding, never by the task's display name."""
    program = task["bind"]["program"]
    total = parse_us(task["bind"]["total_work"])
    if program == "spoof":   # the chrome spoof is one uninterrupted RUN by construction (D7)
        build.program = [{"op": "RUN", "us": total}, {"op": "EXIT"}]
        build.demand_us = total
        return
    runs, blocks = params[f"{program}_run"], params[f"{program}_block"]
    spent, k, ops, pending = 0, 0, [], 0
    while spent < total:
        us = min(max(1, int(sampling.sample(runs, seed, iid, "batch_run", str(k)))), total - spent)
        pending += us
        spent += us
        block = int(sampling.sample(blocks, seed, iid, "batch_block", str(k), allow_zero=True))
        if block >= 1 and spent < total:
            ops.append({"op": "RUN", "us": pending})   # a zero block means the program ran on (D25): the runs it
            ops.append({"op": "SLEEP", "us": block})   # separates join one RUN, the same CPU between two blocks
            pending = 0
        k += 1
    if pending:
        ops.append({"op": "RUN", "us": pending})
    ops.append({"op": "EXIT"})
    build.program, build.demand_us = ops, total


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
    return [{"id": ids[role], "name": names[role], "program": bodies[role]}
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
    names = [task["name"], "wineserver"] + [task["name"]] * (chain_len - 1)
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
        member = _TaskBuild(member_id, names[k])
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
