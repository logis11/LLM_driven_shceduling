# fix-object — a wake held for an unborn spawn-table child

Evidence for the RQ0 gate spec's conformance item (i) (`harness/experiments/rq0-gate.yaml`,
`simulator-conformance`): "a WAKE naming a spawn-table entry reaching that child, a wake sent before
the child's birth held and taken at its birth". Not a trace pair: there is no `expected.csv` and the
trace is not hand-written, so the pair sweeps (`tools/lint.py`, the mock simulator's replay test)
skip this directory by its file names.

- `workload.json` — the simulator's input: one `make` parent whose `spawn_table` holds two object
  jobs built by the dataset's own `compiler._object_job` (the `compiler-child` entry of
  `dataset/archetypes.yaml`, seed 1), six members each (`sh gcc cc1 as fixdep rm`, 9.6 D19), with
  `fork_cap` 8. The parent runs a 500 µs dispatch RUN per job, forks its six members, and ends in
  `EXIT` — not `WAIT children:<id>`, which is conformance (g).
- `reference-trace.jsonl` — `simulator/src/sim workload.json`, no schedule (the boot entry). Byte
  identical across reruns.
- `generate.py` — rebuilds both W fixtures' workloads and traces (`python3 generate.py [sim]`).

## What happens

| µs | |
|---|---|
| 0 | `build` arrives and runs job 1's dispatch RUN |
| 500 | job 1's six members are born (6 of 8 slots) |
| 1000 | job 2's dispatch RUN ends; `build.j2.sh` and `build.j2.gcc` are born — 8 of 8; the third FORK blocks for a slot |
| 6188 | `build.j2.gcc` ends its first RUN and WAKEs `build.j2.cc1`, **not yet born**: the wake is held |
| 457239 | job 1's `sh` ends the job, its six members end, the slots free; `build` forks the remaining four and exits. `build.j2.cc1`'s birth takes the held wake: `task_arrive`, `ready(arrive)`, then a zero-wait `ready(wake)` for its first WAIT (trace lines 93–95) |
| 666567 | job 2 ends — 13 arrivals, 13 `task_end` |

The cap is what makes the hold necessary: `fork_cap` is `parallelism_cap × 6` (9.6 D19, 9.10 D57),
so it can fall mid-job, and a job's members wake each other by spawn-table id.

## Controls

- **Dropping the wake deadlocks the job.** The same binary with the held branch replaced by a drop
  ran 13 arrivals to 7 ends: job 2's six members never end (`simulator/memo/memo_261021.md` E2,
  measured 2026-10-21).
- **Before W the file is refused**: `simulator/steps/sim_v` exits 2 with
  `WAKE target 이 최상위 태스크가 아니다: build.j1.gcc`.
