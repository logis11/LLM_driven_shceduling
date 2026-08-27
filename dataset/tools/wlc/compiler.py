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
  time into chain_length driven members + a near-idle tail.
- The lane-scaling pass (`single` mode) transforms declared-scalable fields
  only — for game-task-chain, chain RUN values are scaled so the chain's
  aggregate demand is lane_share of the lane; nothing else differs from
  `native` output.
"""

import json

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
        "ground_truth": [
            {"t_start": s["t_start"], "t_end": s["t_end"], "mode": s["mode"],
             "attributes": s["attributes"]}
            for s in timeline.segments
        ],
        "events": events,
    }
    duration = timeline.duration_us
    per_task = {b.id: b.demand_us for b in builds}
    report = {
        "duration_us": duration,
        "demand_us": sum(per_task.values()),
        "utilization": sum(per_task.values()) / duration,
        "per_task": per_task,
        "demand_class": timeline.demand_class,
    }
    return canonical, report


def canonical_bytes(canonical):
    """The byte form the manifest hashes and the invariants diff."""
    return (json.dumps(canonical, sort_keys=True, separators=(",", ":"))
            + "\n").encode()


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

    if library.has_input_channel(task["archetype"]):
        _interactive_unroll(build, timeline, task, iid, params, wakes)
    elif _is_fork_loop(program):
        _orchestrator_unroll(build, library, task, iid, seed, params, program)
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

def _orchestrator_unroll(build, library, task, iid, seed, params, program):
    spawn_count = int(task["bind"]["spawn_count"])
    build.fork_cap = int(task["bind"]["parallelism_cap"])
    child_archetype = library.entry(task["archetype"])["spawns"]
    child_entry = library.entry(child_archetype)
    child_name = task["bind"].get("child_name", child_archetype)

    build.spawn_table = []
    for i in range(spawn_count):
        child = _TaskBuild(f"{iid}.c{i + 1}", child_name)
        _spawned_program(child, child_entry, seed, iid, i)
        build.spawn_table.append(
            {"id": child.id, "name": child.name, "program": child.program})
        build.demand_us += child.demand_us

    for i in range(spawn_count):
        us = _draw(params, "dispatch_overhead", seed, iid, i)
        build.program.append({"op": "RUN", "us": us})
        build.program.append({"op": "FORK"})
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
    n_tasks = int(sampling.sample(params["n_tasks"], seed, iid, "n_tasks", 0))
    chain_len = int(sampling.sample(params["chain_length"], seed, iid,
                                    "chain_length", 0))
    frame = sampling.sample(params["frame_period"], seed, iid, "frame_period", 0)

    runs = [sampling.sample(params["per_schedule_run"], seed, iid,
                            "per_schedule_run", k)  # per-task: keyed by member
            for k in range(chain_len)]
    if mode == "single":  # the declared-scalable pass: chain demand -> lane_share
        lane_share = float(task["bind"]["lane_share"])
        factor = lane_share * frame / sum(runs)
        runs = [max(1, round(r * factor)) for r in runs]

    builds = []
    member_ids = [f"{iid}.chain.{k + 1}" for k in range(chain_len)]
    for k, member_id in enumerate(member_ids):
        member = _TaskBuild(member_id, task["name"])
        member.arrive, member.depart = task["arrive"], task["depart"]
        body = ([{"op": "TIMER", "period_us": frame}] if k == 0 else
                [{"op": "WAIT", "channel": f"chain:{member_id}"}])
        body.append({"op": "RUN", "us": runs[k]})
        if k + 1 < chain_len:
            body.append({"op": "WAKE", "target": member_ids[k + 1]})
        member.program = [{"op": "LOOP", "count": "unbounded", "body": body}]
        member.demand_us = round(runs[k] / frame * lifespan)
        builds.append(member)

    for j in range(n_tasks - chain_len):
        tail_id = f"{iid}.tail.{j + 1}"
        tail = _TaskBuild(tail_id, task["name"])
        tail.arrive, tail.depart = task["arrive"], task["depart"]
        gap = sampling.sample(params["tail_idle_gap"], seed, tail_id,
                              "tail_idle_gap", 0)
        run = sampling.sample(params["tail_run"], seed, tail_id, "tail_run", 0)
        tail.program = [{"op": "LOOP", "count": "unbounded",
                         "body": [{"op": "SLEEP", "us": gap},
                                  {"op": "RUN", "us": run}]}]
        tail.demand_us = round(run / (gap + run) * lifespan)
        builds.append(tail)
    return builds
