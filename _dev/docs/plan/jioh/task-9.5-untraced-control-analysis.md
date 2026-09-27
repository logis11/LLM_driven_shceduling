# 9.5 untraced control — analysis tooling, implementation plan

**Goal:** From the control jobs' artifacts, each archetype's per-job ratios (untraced over traced), their reading as 9.7 D36 reads a check, the shares of decisions 10 and 22, and the check of the traced runs against the carried pools — written as a results page per family.

**Architecture:** A shared core, `dataset/tools/meas/control.py`, turns a run's two snapshots into per-thread deltas over the threads alive at both edges, groups them by a family's key, and reads a value's per-job ratios with `check` from `background/pool.py` (the D36 reading) plus the two order groups' means and the interval counts. Each family adds an adapter beside its own tools — `campaign/control.py`, `desktop/control.py`, `session/control.py` — that keys threads exactly as its pool keys components, reads the carried components from the carried pool, and computes the tree-level values. The traced runs go through each family's own `pool.py` under a `--mode control` flag, and the resulting pool is compared with the carried one in standard deviations.

**Tech stack:** Python 3.12, pytest; `dataset/tools/meas/` (campaign, desktop, session, background, stability).

**Spec:** `_dev/docs/spec/jioh/task-9.5-untraced-control.md` (decisions 6–12, 14, 16, 17, 20, 22). Collection plan: `task-9.5-untraced-control.md`.

## Global constraints

- A ratio is the untraced run's value over the traced run's, per job; a value with a zero or missing side in a job has no ratio there.
- Run mean = CPU / voluntary switches (ms); wake rate = voluntary switches / the run's span between its two snapshots (s⁻¹); involuntary switches recorded beside (decision 8).
- Threads keyed `(pid, tid, start_ticks)`; a thread counts only when present at both edges of the run (decision 10).
- The reading is `check` of `background/pool.py` over the per-job ratios; nothing here restates the D36 arithmetic.
- The carried pools stay as they are; the control's traced runs are pooled into a separate record (decision 15).

## Review focus

- A component carried by the pool but absent from a job's snapshots — no ratio for that job, counted.
- A thread reused between the two edges under the same tid — kept apart by `start_ticks`.
- A zero on the traced side (a sparse component that did not wake) — no ratio, not a division error.
- The per-input value when the driven run replayed fewer inputs on one side — the ratio is per input sent, each side by its own count.
- An archetype with no carried component in a phase (the play entries) — tree-level values only.

---

### Task 1: the shared core

**Files:** Create `dataset/tools/meas/control.py`; Test `dataset/tools/tests/test_meas_control.py`.

**Produces:** `thread_deltas(before, after) -> (deltas, span_s)`; `group(deltas, key) -> {component: {run_ns, vol, invol, threads}}`; `rate_and_run(g, span_s) -> (wakes_per_s, run_ms or None)`; `read(pairs) -> dict` where `pairs` is `{job: (order, traced, untraced)}` — `check`'s fields plus `order_means`, `n`.

- [x] Tests: deltas over threads at both edges only, a reused tid kept apart; grouping drops a thread whose key is None; a zero traced side gives no ratio; `read` equals `check` on the same ratios and adds the two order groups' means.
- [x] Implement; tests pass; commit.

### Task 2: 9.5 adapter

**Files:** Create `dataset/tools/meas/campaign/control.py`; Test `test_meas_control.py`.

- [x] Key: the process role from the snapshots' command lines (`analyze.pid_roles`), `analyze.component_name(role, pool.component_key(app, comm))`; `HARNESS_COMMS` and `llvmpipe-*` dropped; the carried pool's `exclude_roles` dropped.
- [x] Carried components per phase from the carried pool (`components.selected`), the rest of the kept threads as `residual`.
- [x] Tree values: per-input run — (tree CPU over the driven run − the same side's idle CPU rate × the run's span) / inputs sent that side; play CPU share — tree CPU / span; operation duration — the mean of the rc-0 durations in `ops.jsonl` / `ops-untraced.jsonl`.
- [x] Tests over a fixture cut from a dry control artifact; commit.

### Task 3: 9.8 and 9.9 adapters

**Files:** Create `dataset/tools/meas/desktop/control.py`, `dataset/tools/meas/session/control.py`; Test `test_meas_control.py`.

- [x] 9.8: renderer subjects keyed per renderer (page renderers of `renderers.tsv`, the control tab dropped as `analyze.drop_control_tab` drops it), a component's wake rate the mean over renderers and its run mean the renderers' pooled CPU over their pooled wakes; the other subjects by role and comm.
- [x] 9.9: instances by `census.ENTRIES` on each process's cgroup and comm, components `<instance>/<comm>`.
- [x] Tests; commit.

### Task 4: the shares of decisions 10 and 22

- [x] From each traced run's trace (the family's analysis rows): per carried component, the share of CPU and wakes held by threads not alive at both edges, and the share a trace-read rule leaves out (9.5 `HEAVY_EVENTS`; 9.9 cron sessions and the causes of D27/D32).
- [x] Tests; commit.

### Task 5: the workload check

- [x] `pool.py --mode control` in campaign, desktop and session: a control artifact accepted, pooled apart.
- [x] Each carried value of the control's pool placed in the carried pool's per-repeat spread in standard deviations; components present in one pool only listed.
- [x] Tests; commit.

### Task 6: the results page

- [x] `control.py <family> <artifacts> <carried pools> <out.json> --md <page>`: per archetype, each value's ratio, interval, reading, medians' ratio, order means, the shares, the interval count and the chance count, the build census, the workload check.
- [ ] Run over the landed control jobs; commit the page to the slice's `campaign/` folder.

### Task 7: the operation windows' share (decision 23)

- [x] `control.shares` takes an `inside` rule beside `left`; the 9.5 adapter's op phase passes the rows `analyze.operation_windows` puts inside the [trigger, done) windows.
- [x] The results page carries the share, CPU and wakes, in its own column for an archetype with an operation phase.
- [x] Tests; commit.
