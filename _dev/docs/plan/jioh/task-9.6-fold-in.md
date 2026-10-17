# 9.6 fold-in — implementation plan

**Goal:** Write the `meas-ci:build:2026-09-18` campaign's measured values and structure into `build-orchestrator`, `compiler-child` and `cpu-batch`, with the compiler support the new structures need.

**Architecture:** Three archetype rewrites in `dataset/archetypes.yaml`, each paired with the compiler path that realises it: the object job becomes six spawn-table entries of `build-orchestrator` wired by WAIT/WAKE (D19), and `cpu-batch` becomes a run-and-block loop over its bound program's measured tables (D21, D22, D25). Values are quantile tables read from `campaign/results/pooled.json`; provenance goes into `validation_stats.scope` and `modeling_notes`.

**Tech stack:** Python 3.12, PyYAML, pytest; `dataset/tools/wlc/` (compiler, sampling, linter, timeline); `make -C dataset`.

**Spec:** `_dev/research/jioh/task-9.6-compile/changelog.md` (D2–D30), with `campaign/method.md` for what was measured and `campaign/results.md` for the values. Phase spec: `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`.

## Global constraints

- **The run-file format is frozen.** Only a top-level task creates tasks; a spawned child has no spawn table of its own. Primitives are RUN, SLEEP, TIMER, WAIT, WAKE, FORK, EXIT; LOOP is VM-internal control flow whose body carries per-task constants. Per-iteration draws are realised by unrolling (`docs/simulator/interpretation-contract.md` §3, §5).
- **Every numeric parameter carries a `source` tag** that resolves in `dataset/sources.yaml`. This campaign's tag is `meas-ci:build:2026-09-18`, which matches the `meas-ci` locator pattern `^[a-z0-9_-]+:(\d+|\d{4}-\d{2}-\d{2})$`.
- **A quantile table is exactly 10 non-decreasing non-negative integers** (p1, p5, p10, p25, p50, p75, p90, p95, p99, p99.9, µs) plus `sampling` and `source` (`dataset/tools/wlc/linter.py:111-115`).
- **A timeline's `bind` keys must equal the archetype's `binding_params`** (`dataset/tools/wlc/timeline.py:102-112`). Adding a binding parameter means editing every timeline that binds the archetype in the same commit.
- **Derived timelines are generated**, never hand-edited: `dataset/timelines/coreset/*.variant.yaml` ops are the source, `python3 tools/derive.py` regenerates.
- **`spawn_count` stays as bound** (인지오, 2026-09-20): the fold-in changes what a job costs, not how many jobs a scenario contains. The resulting demand numbers are recorded and the resizing handed to 9.10.
- **Known-failing check:** five `-single` files sit below the demand window (`c2-p3a`, `c2-p3b`, `c3-creation`, `c3-evening`, `c3-workday`), the branch's declared state until 9.14. `make -C dataset lint` and `check` exit 1 because of them; `make test` passes (the window test is xfail).
- **Commits:** `<type>(jioh/phase-9): …`. Work happens on `jioh/dataset-rebuild`.
- **Checks after each archetype change:** `make -C dataset dataset lint test check PY=python3.12` — `dataset` rewrites `dataset/build/` and `dataset/build.manifest.json`, which are committed.

## File structure

| file | change |
|---|---|
| `dataset/archetypes.yaml` | rewrite the three entries: params, pattern, `validation_stats` (with `scope`), `modeling_notes`, `category_source`, `binding_params` |
| `dataset/tools/wlc/compiler.py` | `_orchestrator_unroll` emits six members per object job; a new `_batch_loop` for `cpu-batch` |
| `dataset/timelines/coreset/*.timeline.yaml` (7 bases) and `c2-pairs.variant.yaml`, `c6.variant.yaml`, `c7.variant.yaml` | add `cpu-batch`'s new `program` bind key |
| `dataset/tools/tests/fixtures/fx-oversub.timeline.yaml` | same bind key |
| `dataset/tools/tests/test_canonical.py` | rewrite `test_orchestrator_spawn_table`; add the batch-loop test |
| `dataset/build/`, `dataset/build.manifest.json`, `dataset/coverage-grid.json` | regenerated |
| `docs/references.md` | the `meas-ci` entry's stale `status:` line |
| `_dev/research/jioh/task-9.6-compile/changelog.md` | the fold-in entry (D31) |

**Value extraction.** Every table below comes from `_dev/research/jioh/task-9.6-compile/campaign/results/pooled.json`. This prints the YAML lines, rounded to integer µs as the linter requires:

```bash
cd /Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling && python3 - <<'EOF'
import json
d = json.load(open('_dev/research/jioh/task-9.6-compile/campaign/results/pooled.json'))
tag = "meas-ci:build:2026-09-18"
def line(name, q, sampling):
    p = [int(round(x)) for x in q]
    assert len(p) == 10 and all(b >= a for a, b in zip(p, p[1:])) and p[0] >= 0, (name, p)
    print(f"        {name}:\n          {{dist: quantiles, p: {p}, sampling: {sampling}, source: \"{tag}\"}}")
w = d['phases']['build-j8-warm']
for k, t in w['object_members']['step_cpu_us'].items():
    role, step = k.split()[0], k.split()[1].split('/')[0]
    line(f"{role}_step_{step}", t['q'], "per-instance")
line("dispatch_overhead", w['dispatch']['per_dispatch_us']['q'], "per-iteration")
for ph, prog in (("clamscan", "clamscan"), ("ffmpeg", "ffmpeg"), ("handbrake", "handbrakecli"),
                 ("train", "python3"), ("tracker", "tracker")):
    s = d['phases'][ph]['shape']
    line(f"{prog}_run", s['runs_between_blocks_us']['q'], "per-iteration")
    line(f"{prog}_block", s['blocks_after_runs_us']['q'], "per-iteration")
EOF
```

---

### Task 1: The object job — six members per spawn-table job

**Files:**
- Modify: `dataset/archetypes.yaml` (`compiler-child`, currently at :690-738)
- Modify: `dataset/tools/wlc/compiler.py:371-392` (`_orchestrator_unroll`), `:395-415` (`_spawned_program` becomes unused for this archetype)
- Test: `dataset/tools/tests/test_canonical.py:31-41` (`test_orchestrator_spawn_table`)

**Interfaces:**
- Consumes: `library.entry("compiler-child")["params"]` — 11 quantile tables named `sh_step_1…4`, `gcc_step_1…3`, `cc1_step_1`, `as_step_1`, `fixdep_step_1`, `rm_step_1`.
- Produces: `_object_job(parent_iid, job_index, child_entry, seed, names) -> (entries, demand_us)` where `entries` is a list of six `{"id", "name", "program"}` dicts in fork order `sh, gcc, cc1, as, fixdep, rm`.

- [ ] **Step 1: Write the failing test**

Replace `test_orchestrator_spawn_table` in `dataset/tools/tests/test_canonical.py`. The fixture `fx-mixed.timeline.yaml` binds `spawn_count: 6, parallelism_cap: 2, child_name: cc1`.

```python
def test_orchestrator_spawn_table_is_six_member_object_jobs():
    # D19: one object job = six spawn-table entries, forked together, woken in D2's parent-child order
    art = _compile_fixture("fx-mixed")
    build = next(e for e in art["events"] if e["op"] == "arrive" and e["id"] == "build")
    assert build["fork_cap"] == 12                      # parallelism_cap 2 x 6 members
    table = build["spawn_table"]
    assert len(table) == 36                             # 6 object jobs x 6 members
    roles = [s["name"] for s in table[:6]]
    assert roles == ["sh", "gcc", "cc1", "as", "fixdep", "rm"]
    by_name = {s["name"]: s for s in table[:6]}
    sh, gcc, cc1 = by_name["sh"], by_name["gcc"], by_name["cc1"]
    assert [op["op"] for op in sh["program"]] == [
        "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "RUN",
        "WAKE", "WAKE", "WAKE", "WAKE", "WAKE", "EXIT"]      # four steps, then it releases the five it held
    assert [op["op"] for op in gcc["program"]] == [
        "WAIT", "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "RUN", "WAKE", "WAIT", "EXIT"]
    assert [op["op"] for op in cc1["program"]] == ["WAIT", "RUN", "WAKE", "WAIT", "EXIT"]
    assert sh["program"][1]["target"] == gcc["id"]      # sh wakes gcc first (D2's order)
    assert gcc["program"][2]["target"] == cc1["id"]     # gcc wakes cc1, then as, then sh
    assert cc1["program"][0]["channel"] == f"job:{cc1['id']}"
    assert 300_000 < cc1["program"][1]["us"] < 700_000  # cc1 dominates the job (p50 368 ms)
    assert len({s["id"] for s in table}) == 36
```

- [ ] **Step 2: Run it and watch it fail**

```bash
cd dataset/tools && python3.12 -m pytest tests/test_canonical.py::test_orchestrator_spawn_table_is_six_member_object_jobs -q
```
Expected: FAIL — today's table has 6 entries named `cc1` and `fork_cap` 2.

- [ ] **Step 3: Write `compiler-child`'s new parameters**

Run the extraction command from **File structure** and paste its first 11 lines into `compiler-child.params`, replacing `cpu_burst`, `cpu_tail` and `disk_wait`. The entry's other fields in this task: `pattern.program` documents the member shape, `lifetime: spawned`, `spawned_by: build-orchestrator` stay. `sh_step_1` for reference — the extraction prints the rest in the same shape:

```yaml
      sh_step_1:
        {dist: quantiles, p: [663, 688, 700, 725, 766, 803, 832, 853, 902, 1051], sampling: per-instance, source: "meas-ci:build:2026-09-18"}
```

Replace `pattern` with the job's shape as documentation (the compiler builds the members; `pattern.program` is not interpreted for spawned children):

```yaml
    pattern:
      program:                 # D19: one object job, six members forked together, woken in D2's order
        - sh: [RUN, WAKE gcc, WAIT, RUN, WAKE fixdep, WAIT, RUN, WAKE rm, WAIT, RUN, WAKE each member, EXIT]
        - gcc: [WAIT, RUN, WAKE cc1, WAIT, RUN, WAKE as, WAIT, RUN, WAKE sh, WAIT, EXIT]
        - cc1: [WAIT, RUN, WAKE gcc, WAIT, EXIT]
        - as: [WAIT, RUN, WAKE gcc, WAIT, EXIT]
        - fixdep: [WAIT, RUN, WAKE sh, WAIT, EXIT]
        - rm: [WAIT, RUN, WAKE sh, WAIT, EXIT]
```

- [ ] **Step 4: Write the constructor in the compiler**

In `dataset/tools/wlc/compiler.py`, above `_orchestrator_unroll`:

```python
# D19, D20: one make job as six member processes — the roles in fork order, each with its structural step count
OBJECT_JOB = (("sh", 4), ("gcc", 3), ("cc1", 1), ("as", 1), ("fixdep", 1), ("rm", 1))


def _object_job(parent_iid, job_index, child_entry, seed, child_name):
    """One object job as six spawn-table entries (D19): `sh` runs first, each other member waits on its own channel
    and is woken in the job's parent-child order (D2) — sh, gcc, cc1, gcc, as, gcc, sh, fixdep, sh, rm, sh — each
    member's step CPU drawn from its own (role, step) table (D20). A member that has finished waits, without CPU,
    until `sh` ends the job, so `fork_cap` bounds the jobs in flight."""
    params = child_entry["params"]
    ids = {role: f"{parent_iid}.j{job_index + 1}.{role}" for role, _ in OBJECT_JOB}
    names = dict.fromkeys(ids, None) | {role: role for role, _ in OBJECT_JOB} | {"cc1": child_name}
    demand = 0
    def run(role, step):
        nonlocal demand
        us = int(sampling.sample(params[f"{role}_step_{step}"], seed, parent_iid,
                                 "job", str(job_index), role, str(step)))
        demand += us
        return {"op": "RUN", "us": us}
    wait = lambda role: {"op": "WAIT", "channel": f"job:{ids[role]}"}
    wake = lambda role: {"op": "WAKE", "target": ids[role]}
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
    return [{"id": ids[role], "name": names[role], "program": bodies[role]} for role, _ in OBJECT_JOB], demand
```

Then rewrite the body of `_orchestrator_unroll` (keep its signature):

```python
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

    for i in range(spawn_count):      # one dispatch run per job, then the job's six members are forked together
        us = _draw(params, "dispatch_overhead", seed, iid, i)
        build.program.append({"op": "RUN", "us": us})
        build.program.extend([{"op": "FORK"}] * len(OBJECT_JOB))
        build.demand_us += us
    build.program.append({"op": "WAIT", "channel": f"children:{iid}"})
    build.program.append({"op": "EXIT"})
```

- [ ] **Step 5: Run the test and the suite**

```bash
cd dataset/tools && python3.12 -m pytest tests/test_canonical.py -q && python3.12 -m pytest tests -q
```
Expected: the new test passes. `test_invariants.py` and `test_coreset.py` must stay green; if `test_demand_estimate` moves, that is this change and its new value goes in the assertion with a comment naming D19.

- [ ] **Step 6: Commit**

```bash
git add dataset/archetypes.yaml dataset/tools/wlc/compiler.py dataset/tools/tests/test_canonical.py
git commit -m "feat(jioh/phase-9): 9.6 fold-in D19–D20 — one object job is six spawn-table entries wired by WAIT/WAKE, each member's step CPU from its measured table; fork_cap is the cap times six"
```

---

### Task 2: `build-orchestrator`'s dispatch table, and both build archetypes' provenance

**Files:**
- Modify: `dataset/archetypes.yaml` (`build-orchestrator` :740-786, and `compiler-child`'s prose fields)

**Interfaces:**
- Consumes: Task 1's `OBJECT_JOB` and the extraction command's `dispatch_overhead` line.
- Produces: nothing code-facing; the entries' `validation_stats.scope` and `modeling_notes` that later tasks cite.

- [ ] **Step 1: Replace `dispatch_overhead` with the measured table**

```yaml
      dispatch_overhead:
        {dist: quantiles, p: [118, 227, 246, 387, 676, 889, 1129, 1329, 1679, 2704], sampling: per-iteration, source: "meas-ci:build:2026-09-18"}
```

Keep `binding_params: [spawn_count, parallelism_cap, child_name]` and `spawns: compiler-child`. Change `category_source` from `ocallahan-atc17` to `meas` on both entries (D2: the class's existence is literature, the values and structure are this observation).

- [ ] **Step 2: Write `build-orchestrator`'s `validation_stats`**

```yaml
    validation_stats:
      referee: meas-ci
      run: "build:2026-09-18, repeats [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]"
      stats: ["dispatch run per job p50 676 us, mean 691 us (+-0.94 %)", "5 957 forks under 716 make processes per build",
              "5 254 jobs per build: 2 908 object, 681 archive, 1 537 helper, 90 probe, 38 link",
              "live jobs at cap 8: mean 7.87, peak 11"]
      scope: >-
        One observation (phase decision 2; D3, D5, D30): GNU make 4.3 building linux-6.6 defconfig with `make -j8`,
        warm, on a GitHub-hosted ubuntu-24.04 runner (4 vCPU AMD EPYC 7763, kernel 6.17.0-1022-azure) pinned to one
        CPU, instrumented by `perf sched record` on the measured CPU and a taskstats listener on its cpumask. 14
        same-machine repeats under the machine gate; the stability rule holds (D26, D30). Dispatch run is make's own
        CPU between consecutive fork events, pooled over every make of the build (D8 iv). `-j8` on one CPU costs
        about 10 % more CPU per compile than `-j1` (D4, D9), a stated limitation of these values. Values are this
        software on this machine, not desktop truth (9.5 D10).
    modeling_notes: >-
      FORK consumes a pre-sampled ordered spawn table; one dispatch run precedes each job's six FORKs (D19).
      `spawn_count` counts object jobs and `parallelism_cap` counts jobs, as make's jobserver counts them; the
      compiler multiplies the cap by the six members for `fork_cap` (D19). `parallelism_cap` defaults to 8 by the
      `nproc` rule applied to an eight-thread desktop, overridable at binding time (D4). The DKMS binding describes
      an out-of-tree kbuild run whose per-object CPU is assumed to follow the kernel's; no observation of a DKMS
      run's duration, CPU or process count exists (D6). Unmodelled per build: 681 archive, 1 537 helper, 90 probe
      and 38 link jobs under 716 make processes, together under 3 % of the build's CPU, their proportions kbuild's
      for this tree (D9).
```

- [ ] **Step 3: Write `compiler-child`'s `validation_stats` and `modeling_notes`**

```yaml
    validation_stats:
      referee: meas-ci
      run: "build:2026-09-18, repeats [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]"
      stats: ["2 857 six-member object jobs per build in every repeat", "child order sh: gcc fixdep rm; gcc: cc1 as, 2 857 each",
              "cc1 CPU per process mean 435.0 ms (+-0.78 %)", "step CPU half-widths +-0.7 to 1.4 %",
              "cc1 wakes once in 99.3 % of jobs; sh 5-7 times, gcc 4-7"]
      scope: >-
        One observation (phase decision 2; D3, D30): the object jobs of the same warm `-j8` linux-6.6 defconfig
        build as `build-orchestrator`, gcc 13.2.0 on Ubuntu 24.04, no `-pipe` in the kernel's Makefile so `cc1` and
        `as` run in sequence. Per-process CPU is the sum of the process's perf segments on the measured CPU, with
        taskstats exit accounting as the cross-check (perf over taskstats 1.005 for `cc1`); step CPU is the sum of a
        member's runs between its children's forks and exits (D20). Warm: no block-I/O delay per process. Under the
        cold cache `cc1` wakes twice at the median with a 183 us disk wait per wake, reported beside the pool and
        not carried (D8 iii, D9). Values are this software on this machine, not desktop truth (9.5 D10).
    modeling_notes: >-
      One make job is the chain of processes it runs, one task per process (D2). In the frozen format only a
      top-level task creates tasks, so the job is six consecutive spawn-table entries of `build-orchestrator` rather
      than a child with its own spawn table (D19). Each member runs once per structural step, the steps bounded by
      its children's forks and exits (D20): `sh` four, `gcc` three, the others one. Against the records `sh` wakes
      5-7 times and `gcc` 4-7, so the model's four and three are the structure, not the wake count; steps and
      members draw independently. A member that has finished waits without CPU until `sh` ends the job, so a
      member's trace arrival and end are its job's, not its process lifetime: its `turnaround` row is reported
      unweighted, no scored term reads it, and a waiting member accrues no `ready_wait` (D19). The recognizer's view
      is unchanged: the visible projection carries spawn-table names and counts attributed to the parent's lifetime
      (D19). The kernel-build literature grounds the class's existence and short-lived character only (D2).
```

- [ ] **Step 4: Lint and rebuild**

```bash
cd dataset && python3.12 tools/lint.py; python3.12 tools/derive.py && python3.12 tools/compile.py
```
Expected: lint reports only the five known `-single` demand files. The compile rewrites `dataset/build/` and the manifest.

- [ ] **Step 5: Commit**

```bash
git add dataset/archetypes.yaml dataset/build dataset/build.manifest.json
git commit -m "feat(jioh/phase-9): 9.6 fold-in — build-orchestrator carries the measured dispatch table; both build archetypes carry the campaign's scope and modeling notes"
```

---

### Task 3: `cpu-batch` — the run-and-block loop over a bound program's tables

**Files:**
- Modify: `dataset/archetypes.yaml` (`cpu-batch` :662-688)
- Modify: `dataset/tools/wlc/compiler.py` (`_compile_instance` dispatch, new `_batch_loop`)
- Modify: 7 base timelines, `c2-pairs.variant.yaml`, `c6.variant.yaml`, `c7.variant.yaml`, `dataset/tools/tests/fixtures/fx-oversub.timeline.yaml`
- Test: `dataset/tools/tests/test_canonical.py`

**Interfaces:**
- Consumes: the extraction command's ten `<program>_run` / `<program>_block` tables.
- Produces: binding parameter `program`, one of `clamscan`, `ffmpeg`, `handbrakecli`, `python3`, `tracker`, `spoof`; `_batch_loop(build, entry, task, seed, iid)`.

- [ ] **Step 1: Write the failing test**

```python
def test_cpu_batch_runs_and_blocks_until_total_work():
    # D21, D22, D25: RUN drawn from the program's runs between voluntary blocks, then the block that followed it
    art = _compile_fixture("fx-oversub")
    task = next(e for e in art["events"] if e["op"] == "arrive" and e["id"] == "train")
    ops = [op["op"] for op in task["program"]]
    assert ops[-1] == "EXIT" and ops.count("RUN") > 1          # a loop, not one uninterrupted RUN
    assert set(ops) == {"RUN", "SLEEP", "EXIT"}
    assert sum(op["us"] for op in task["program"] if op["op"] == "RUN") == 66_000_000   # total_work exactly
    assert all(op["us"] >= 1 for op in task["program"] if op["op"] in ("RUN", "SLEEP"))
```

- [ ] **Step 2: Run it and watch it fail**

```bash
cd dataset/tools && python3.12 -m pytest tests/test_canonical.py::test_cpu_batch_runs_and_blocks_until_total_work -q
```
Expected: FAIL — today the program is one RUN of `total_work` then EXIT.

- [ ] **Step 3: Write `cpu-batch`'s parameters and pattern**

Paste the extraction command's ten batch lines into `params`. `binding_params` becomes `[total_work, program]`. Pattern:

```yaml
    pattern:
      constructor: batch-loop     # D21: RUN from the bound program's runs between voluntary blocks, then its block
      program:
        - loop:
            - RUN: run_between_blocks
            - SLEEP: block_after_run
        - EXIT: {}
```

- [ ] **Step 4: Write the constructor**

In `compiler.py`, extend the constructor dispatch at `:114-117`:

```python
    entry = library.entry(task["archetype"])
    constructor = entry["pattern"].get("constructor")
    if constructor == "chain":
        return _chain_constructor(timeline, task, iid, entry, mode)
    if constructor == "batch-loop":
        build = _TaskBuild(iid, task["name"])
        build.arrive = task["arrive"]
        _batch_loop(build, entry, task, timeline.seed, iid)
        return [build]
```

and add:

```python
def _batch_loop(build, entry, task, seed, iid):
    """D21, D22, D25: the bound program's measured run between voluntary blocks, then the off-CPU time that followed
    that run — zero-inclusive, so a zero block means another thread of the program ran on — until `total_work` of CPU
    is spent. The table set is chosen by the `program` binding, never by the task's display name (D21)."""
    program = task["bind"]["program"]
    total = _duration_us(task["bind"]["total_work"])
    if program == "spoof":       # the chrome spoof is one uninterrupted RUN by construction (D7)
        build.program = [{"op": "RUN", "us": total}, {"op": "EXIT"}]
        build.demand_us = total
        return
    runs, blocks = entry["params"][f"{program}_run"], entry["params"][f"{program}_block"]
    spent, k, ops = 0, 0, []
    while spent < total:
        us = min(max(1, int(sampling.sample(runs, seed, iid, "batch_run", str(k)))), total - spent)
        ops.append({"op": "RUN", "us": us})
        spent += us
        if spent < total:
            block = int(sampling.sample(blocks, seed, iid, "batch_block", str(k)))
            if block >= 1:
                ops.append({"op": "SLEEP", "us": block})
        k += 1
    ops.append({"op": "EXIT"})
    build.program, build.demand_us = ops, total
```

Use the same duration parser the existing `cpu-batch` path uses for `total_work`; if that path inlined it, lift it into `_duration_us` and call it from both.

- [ ] **Step 5: Add the binding to every timeline that binds `cpu-batch`**

Bases: `c2-p1a` → `program: python3`; `c1-indexing` → `tracker`; `c1-ml-train` → `python3`; `c1-render` → `ffmpeg`; `c1-transcode` → `handbrakecli`; `c2-p3a` → `ffmpeg`; `c3-creation` → `handbrakecli`. Fixture `fx-oversub` → `python3`.

Variant ops: `c2-pairs.variant.yaml` — the `c2-p1b` op is rename-only, so it inherits `program: python3` and the pair stays byte-identical apart from the label (D21's hand-off to 9.10 is whether it later takes `tracker`'s tables); the `c2-p2b` op that replaces the download with `clamscan` sets `program: clamscan`. `c6.variant.yaml` — the spoof op sets `program: spoof`. `c7.variant.yaml` — each injected `clamscan` op sets `program: clamscan`; the four same-name counterparts inherit their base.

- [ ] **Step 6: Regenerate, test, lint**

```bash
cd dataset && python3.12 tools/derive.py && python3.12 tools/compile.py && python3.12 -m pytest tools/tests -q && python3.12 tools/lint.py
```
Expected: `test_p1_pair_rename_only` and the C7 counterpart tests stay green; `test_demand_estimate` unchanged, because blocks add no CPU and `demand_us` is still `total_work`.

- [ ] **Step 7: Commit**

```bash
git add dataset/archetypes.yaml dataset/tools/wlc/compiler.py dataset/timelines dataset/tools/tests dataset/build dataset/build.manifest.json dataset/coverage-grid.json
git commit -m "feat(jioh/phase-9): 9.6 fold-in D21–D22, D25 — cpu-batch draws its bound program's measured runs and the block after each, chosen by an explicit binding; the chrome spoof stays one RUN"
```

---

### Task 4: `cpu-batch`'s provenance

**Files:**
- Modify: `dataset/archetypes.yaml` (`cpu-batch`'s `category_source`, `validation_stats`, `modeling_notes`)

- [ ] **Step 1: Replace `category_source` and `validation_stats`**

`category_source: meas` (D7: interbench Burn leaves with the emulation).

```yaml
    validation_stats:
      referee: meas-ci
      run: "build:2026-09-18; repeats [4, 5, 7, 8, 9-18]; clamscan [9-18], python3 [11-18]"
      stats: ["saturation over the job: clamscan 0.971-0.979, ffmpeg 0.9996, HandBrakeCLI 0.990-0.993, python3 0.9997, tracker 0.941-0.962",
              "share of CPU past the 10 ms boot slice: 0.109, 0.698, 0.626, 0.998, 0.532",
              "share of runs followed by a block: 1.0, 0.0015, 0.0008, 1.0, 0.16",
              "block per run carried with its half-width (D29): clamscan 218.1 us +-9.5 %, python3 220.0 us +-14.0 %, tracker 17.6 us +-15.1 %"]
      scope: >-
        One observation (phase decision 2; D3, D7, D30): five programs measured in the same campaign as the build
        archetypes, each pinned to one CPU of a GitHub-hosted ubuntu-24.04 runner (4 vCPU AMD EPYC 7763, kernel
        6.17.0-1022-azure) — ClamAV 1.5.3 scanning the kernel's `Documentation` (9 462 files) with signature
        database daily 28128 held fixed from repeat 9 (D27); ffmpeg and HandBrakeCLI encoding a generated 60 s clip;
        a PyTorch 2.14 CPU training loop of 300 steps, started warm so its measured runs and blocks are the training
        job's and not the interpreter's first page-ins (D28); Tracker 3.7.1 indexing a copy of the same corpus, read
        over its job window from the miner's first schedule-in to its own Idle status (D16). Runs are the CPU from
        one voluntary block to the next, pooled over the program's threads; the block after a run is the program's
        off-CPU time that followed it, zero when another thread ran on (D22, D25). Four values' spread follows the
        runner's disk rather than the program and is carried with its half-width instead of the 5 % tolerance (D29);
        their blocks are 2.4 % (clamscan), 4 % (tracker) and 0.01 % (python3) of each job's time. Values are this
        software on this machine, not desktop truth (9.5 D10).
```

- [ ] **Step 2: Replace `modeling_notes`**

```yaml
    modeling_notes: >-
      The class is what the measurement shows: five programs runnable for the whole of their job on one dominant
      thread (D7, D16). The task is a loop — a run drawn from the bound program's measured runs between voluntary
      blocks, then the block that followed such a run — until `total_work` of CPU is spent; the table set is chosen
      by the `program` binding, never by the task's display name (D21). A multi-threaded program is one task: runs
      pooled over its threads, blocks the program's own off-CPU time, so the task alternates the threads' long and
      short runs in one sequence and cannot show a main thread demoted while its workers keep their level (D22).
      `total_work` is scenario design and binds in the timeline (D7). The `chrome` spoof is one uninterrupted RUN by
      construction (D7). The `tracker-miner-fs-3` binding's real processes declare themselves background work —
      every thread exits with policy SCHED_IDLE at nice 19, while clamscan, ffmpeg, HandBrakeCLI and python3 run at
      the default policy — and the task model carries no declared class, so a simulated baseline cannot honour it
      (D17; handed to 9.11). Its tail after the job, about 0.35 s of CPU over 10-15 s, is the everyday daemon and
      outside this binding (D16).
```

- [ ] **Step 3: Lint, rebuild, commit**

```bash
cd dataset && python3.12 tools/lint.py; python3.12 tools/compile.py
cd .. && git add dataset/archetypes.yaml dataset/build dataset/build.manifest.json
git commit -m "feat(jioh/phase-9): 9.6 fold-in D7, D16–D17, D29 — cpu-batch carries the campaign's scope, the declared-class note and the four stated half-widths"
```

---

### Task 5: Registry lines and the fold-in record

**Files:**
- Modify: `docs/references.md` (the `meas-ci` entry, :302)
- Modify: `_dev/research/jioh/task-9.6-compile/changelog.md`
- Check: `dataset/sources.yaml` (`interbench` :47, `ananicy-rules` :164 — they stay while the IO family still uses them; 9.7's fold-in removes them if it removes the last user)

- [ ] **Step 1: Correct the `meas-ci` status line**

Its `status:` still reads "reserved (no runs yet; `meas-pending` placeholders in archetypes until freeze)". Replace with the campaign form (9.7 D17 hands this to whichever measured slice folds in first):

```
- status: in use — one release per campaign, each repeat's run id in the pooled record and in the archetype's `validation_stats.run`; the campaign workflow is `_dev/research/jioh/measurement-campaign-workflow.md`
```

- [ ] **Step 2: Run the full check**

```bash
make -C dataset dataset lint test check PY=python3.12
```
Record: the manifest's new `utilization` per file, which files the demand window now fails and in which direction.

- [ ] **Step 3: Write the changelog entry**

Append D31 — what the fold-in applied (D2, D7, D9, D16–D22, D25, D27–D30), the artifacts rebuilt, the demand numbers before and after, the new known-failing set, and the hand to 9.10 that `spawn_count` was sized against the old per-child cost of about 89 ms while a job now costs about 471 ms.

- [ ] **Step 4: Commit and push**

```bash
git add docs/references.md _dev/research/jioh/task-9.6-compile/changelog.md dataset
git commit -m "chore(jioh/phase-9): 9.6 fold-in recorded — D31; meas-ci's registry line; the demand state after the rebuild"
git push
```

## Self-review

- **Coverage.** D2 (the unit, `category_source`) Task 1–2; D3, D5, D30 (observation, repeats) scope fields Tasks 2, 4; D4 (cap default, `-j1` limitation) Task 2; D6 (DKMS) Task 2; D7 (bound programs, `total_work`, spoof) Tasks 3–4; D8 (quantile tables, no warm disk wait) Tasks 1–2; D9 (unmodelled job kinds) Task 2; D16 (tracker's job window) Task 4; D17 (SCHED_IDLE) Task 4; D19 (six entries, `fork_cap`, turnaround) Task 1; D20 (steps) Task 1; D21, D22, D25 (loop, one task, block draw) Task 3–4; D26–D30 (rule, database, warm start, half-widths, final pool) scope and stats fields Tasks 2, 4; registry lines Task 5.
- **Not in scope, handed on:** `spawn_count` resizing and whether `c2-p1b` takes `tracker`'s tables (9.10); the demand-window rule (9.14); the five member names' effect on the coverage grid's familiarity tier, which counts only the orchestrator's `child_name` today (9.10, 9.14); the raw-record release and wrap-up, which follow this plan.
- **Type consistency.** `OBJECT_JOB` is defined in Task 1 and used in Tasks 1 and 3's `fork_cap` reasoning; `_batch_loop` and the `program` binding values are defined in Task 3 and cited in Task 4's notes; parameter names (`<role>_step_<n>`, `<program>_run`, `<program>_block`) are produced by the extraction command in **File structure** and consumed in Tasks 1–3.
