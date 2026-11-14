#!/usr/bin/env python3
"""Conformance items (i) and (g) of the RQ0 gate spec (harness/experiments/rq0-gate.yaml,
`simulator-conformance`), black-box on the binary, and what the two reference fixtures' worked.md
read off them (harness/tools/tests/fixtures/fix-object, fix-tree).

    python3 simulator/tests/test_spawn_children.py [path/to/sim]      # default simulator/src/sim

(i) A WAKE naming a spawn-table entry reaches that child; a wake sent before the child's birth is
    held and taken at its birth. On each reference workload, run as its reference trace was (the
    boot entry alone as its schedule, harness/boot-defaults/ostep.json at t = 0, provenance
    fallback): every WAKE a spawned member sends a sibling before the first block of its program
    is placed in time from the trace — the instant the member's lane time reaches the RUNs before
    it — and each one sent before the sibling's birth is a held wake, which the sibling takes at
    its birth: its task_arrive, ready(arrive) and a zero-wait ready(wake) for its first WAIT at that
    µs. The pair the worked.md names (build.j2.gcc's wake of build.j2.cc1) is among them. Every
    arrival is matched by exactly one task_end, so every job completes.
(g) An orchestrator's WAIT children:<id> completes when every child it spawned has ended: on each
    reference workload `build`'s ready(wake) comes at its last child's task_end, after it in the
    trace, and its task_end follows at the same µs. And without blocking when none is live at the
    WAIT: a hand workload whose one child ends while the parent is still running reaches the WAIT
    inside the parent's occupancy — a zero-wait ready(wake) at the instant its lane time reaches
    its RUNs, no block, and the parent runs on to its end.
"""
import json
import os
import sys

import blackbox as bb

FIXTURES = os.path.join(bb.ROOT, "harness", "tools", "tests", "fixtures")
NAMED = {"fix-object": ("build.j2.gcc", "build.j2.cc1"), "fix-tree": ("build.j2.gcc", "build.j2.cc1")}
BOOT = os.path.join(bb.ROOT, "harness", "boot-defaults", "ostep.json")


def reference_run(sim, name):
    with open(os.path.join(FIXTURES, name, "workload.json")) as f:
        wl = json.load(f)
    with open(BOOT) as f:
        boot = json.load(f)
    entries = [{"t_us": 0, "config": boot, "provenance": "fallback"}]
    return wl, bb.run(sim, wl["meta"]["id"], wl["events"], entries)


def early_wakes(prog):
    """(lane time before it, target) for each WAKE ahead of the program's first WAIT that blocks
    after a RUN — straight-line only, the prefix a trace can place without following a loop."""
    out, ran, seen_run = [], 0, False
    for ins in prog:
        if ins["op"] == "RUN":
            ran += ins["us"]; seen_run = True
        elif ins["op"] == "WAKE":
            out.append((ran, ins["target"]))
        elif ins["op"] == "WAIT" and seen_run:
            break
        elif ins["op"] not in ("WAIT",):
            break
    return out


def check_reference(sim, name):
    wl, tr = reference_run(sim, name)
    parent = next(e for e in wl["events"] if e["op"] == "arrive" and e.get("spawn_table"))
    table = {c["id"]: c for c in parent["spawn_table"]}
    born = {e["task"]: e["t"] for e in tr if e["event"] == "task_arrive"}
    held = []
    for sid, c in table.items():
        for ran, target in early_wakes(c["program"]):
            if target not in table:
                continue
            sent = bb.cpu_reached(tr, sid, ran)
            if sent is None:              # never sent: a member left waiting, which the end count below names
                continue
            if sent < born[target]:
                held.append((sid, target, sent, born[target]))
    assert held, f"{name}: no wake reached a spawn-table child before its birth — (i)'s case is not exercised"
    for waker, target, sent, birth in held:
        lines = [(e["event"], e.get("cause")) for e in tr if e.get("task") == target and e["t"] == birth]
        assert lines[:3] == [("task_arrive", None), ("ready", "arrive"), ("ready", "wake")], (
            f"{name}: {target}, woken by {waker} at {sent} µs before its birth at {birth} µs, did not take the "
            f"wake at its birth — its lines then: {lines}")
    assert NAMED[name][:2] in [(w, t) for w, t, _s, _b in held], f"{name}: the worked.md's pair {NAMED[name]} is not a held wake"
    arrivals = [e["task"] for e in tr if e["event"] == "task_arrive"]
    ends = [e["task"] for e in tr if e["event"] == "task_end"]
    assert sorted(arrivals) == sorted(ends) and len(set(ends)) == len(ends), (
        f"{name}: {len(arrivals)} arrivals, {len(ends)} task_end lines — never ended: "
        f"{sorted(set(arrivals) - set(ends))[:4]}")
    # (g): the children wait
    pid = parent["id"]
    kids = [e["task"] for e in tr if e["event"] == "task_arrive" and e.get("parent") == pid]
    kid_ends = [(i, e) for i, e in enumerate(tr) if e["event"] == "task_end" and e["task"] in kids]
    last_i, last = max(kid_ends, key=lambda p: (p[1]["t"], p[0]))
    wake = [(i, e) for i, e in enumerate(tr) if e["event"] == "ready" and e["task"] == pid and e["cause"] == "wake"]
    assert len(wake) == 1, f"{name}: {pid} has {len(wake)} ready(wake) lines, not the one of its children wait"
    wi, w = wake[0]
    assert w["t"] == last["t"] and wi > last_i, (
        f"{name}: {pid}'s children wait completed at {w['t']} µs (line {wi + 1}), not at its last child's "
        f"task_end at {last['t']} µs (line {last_i + 1})")
    end = next(e for e in tr if e["event"] == "task_end" and e["task"] == pid)
    assert end["t"] == last["t"], f"{pid} ended at {end['t']} µs, not at its children wait's completion"
    return (f"{name}: {len(held)} held wake(s), {NAMED[name][1]} at {born[NAMED[name][1]]} µs; "
            f"{len(arrivals)} arrivals, {len(ends)} ends; {pid}'s wait done at {w['t']} µs")


def test_reference_fixtures(sim):
    return "; ".join(check_reference(sim, n) for n in sorted(NAMED))


def test_children_wait_with_none_live(sim):
    child = {"id": "kid", "name": "kid", "program": [{"op": "RUN", "us": 1_000}, {"op": "EXIT"}]}
    prog = [{"op": "FORK"}, {"op": "RUN", "us": 50_000}, {"op": "WAIT", "channel": "children:par"},
            {"op": "RUN", "us": 1_000}, {"op": "EXIT"}]
    ev = [{"op": "arrive", "t": 0, "id": "par", "name": "par", "fork_cap": 1, "spawn_table": [child], "program": prog}]
    tr = bb.run(sim, "children-none-live", ev, [bb.entry("MLFQ")])
    kid_end = next(e["t"] for e in tr if e["event"] == "task_end" and e["task"] == "kid")
    reached = bb.cpu_reached(tr, "par", 50_000)
    assert kid_end < reached, f"the child ended at {kid_end} µs, not before the parent reached its WAIT at {reached}"
    wakes = [e["t"] for e in tr if e["event"] == "ready" and e["task"] == "par" and e["cause"] == "wake"]
    assert wakes == [reached], f"the parent's ready(wake) lines {wakes}, not one at {reached} µs"
    blocks = [e for e in tr if e["event"] == "run_end" and e["task"] == "par" and e["reason"] == "block"]
    assert not blocks, f"the parent blocked: {blocks}"
    inside = [(s, e) for t, s, e, _ in bb.occupancies(tr) if t == "par" and s <= reached < e]
    assert inside, f"the parent did not hold the lane across {reached} µs: its WAIT was not passed inside an occupancy"
    end = next(e for e in tr if e["event"] == "task_end" and e["task"] == "par")
    assert end["reason"] == "exit" and bb.cpu(tr, "par") == 51_000, "the parent did not run on to its EXIT"
    return f"the child ended at {kid_end} µs; the WAIT passed at {reached} µs with a zero-wait ready(wake)"


if __name__ == "__main__":
    sys.exit(bb.main([("i+g-reference", test_reference_fixtures),
                      ("g-none-live", test_children_wait_with_none_live)], sys.argv))
