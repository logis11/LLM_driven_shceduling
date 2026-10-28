# fix-tree — a wake held for an unborn spawn-table child, module-build trees

The second fixture for conformance item (i); read `../fix-object/worked.md` first, whose
conventions this one shares. `../fix-object/generate.py` rebuilds both.

- `workload.json` — one `make` parent whose `spawn_table` holds two module-build trees built by
  `compiler._tree_job` (the `module-compiler-child` entry of `dataset/archetypes.yaml`, seed 1):
  `conftest_a` with 8 members and `conftest_b` with 10 (9.10 D53), `fork_cap` 12. As in
  `fix-object`, a 500 µs dispatch RUN per job and `EXIT`, not `WAIT children:<id>`.
- `reference-trace.jsonl` — `simulator/src/sim workload.json`, no schedule. Byte identical across
  reruns.

## What happens

| µs | |
|---|---|
| 500 | job 1's eight members are born (8 of 12 slots) |
| 1000 | job 2's first four members are born — 12 of 12; the fifth FORK blocks for a slot |
| 11650 | `build.j2.gcc` ends its first RUN and WAKEs `build.j2.cc1`, **not yet born**: the wake is held |
| 164256 | job 1 ends, the slots free; `build` forks job 2's last six and exits. `build.j2.cc1`'s birth takes the held wake (`ready(arrive)`, then a zero-wait `ready(wake)`) |
| 190037 | job 2 ends — 19 arrivals, 19 `task_end` |

The trees are 8 and 10 members while `fork_cap` is a multiple of six in the dataset, so a cap
always splits one of them; 12 here splits the second.

## Controls

- **Dropping the wake**: 19 arrivals, 9 ends — job 2's ten members never end
  (`simulator/memo/memo_261021.md` E2).
- **Before W**: `simulator/steps/sim_v` exits 2 with
  `WAKE target 이 최상위 태스크가 아니다: build.j1.csh`.
