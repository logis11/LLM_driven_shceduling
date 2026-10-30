# 2026-10-31 demotion edges

The RQ0 gate spec's boot-default sweep re-picked at the demotion edges per 100 ms boost interval (decided 2026-10-30, `_dev/TODO.md` Phase 10). Under the allotment kept across bursts (`simulator/memo/memo_261023.md` Part H3; OSTEP §8.4's Rule 4; the simulator guide §5 rule 4) a task is demoted from the top queue in a boost interval when its CPU there since the boost reaches the slice.

The simulator is the reference simulator, `simulator/src/sim.cpp` at commit `8dab1176`, built with `c++ -std=c++17 -O2`. The workloads are `dataset/build/coreset-single/` at the dataset manifest the RQ0 gate spec pins. The schedule is the `fixed` condition on `harness/boot-defaults/ostep.json` with only `timeslice_us` changed. The traces (about 20 MB each) are not kept; the scripts regenerate them, from the repository root:

```
bash _dev/research/jioh/2026-10-31-demotion-edges/sweep.sh OUT SIM > table.md
python3 _dev/research/jioh/2026-10-31-demotion-edges/edges.py OUT > edges.md
bash _dev/research/jioh/2026-10-31-demotion-edges/fixed_check.sh OUT SIM PY > fixed-check.md
```

## Files

- `run.sh`: one core-set file at one top slice.
- `sweep.sh`: `c1-meeting`, `c1-media`, `c1-gaming` and `c2-p2a` at 17 top slices, then `table.py`.
- `table.py` → `table.md`: per file and slice, the share of a task's boost intervals (those wholly inside its life) holding at least one `x_mlfq_demote` line of it, the intervals read off the `x_mlfq_boost` lines. For the two gaming files, the count of the frame chain's 17 tasks (16 members and the wineserver) demoted in at least half of their intervals, and in any.
- `edges.py` → `edges.md`: each task's CPU per boost interval, its run segments summed per interval on the 100 000 µs run, where nothing is demoted. The mean is the edge the RQ0 gate spec states.
- `fixed_check.sh`, `fixed_check.py` → `fixed-check.md`: files under `fixed` at 10 000 µs. For `c7-meeting` and `c7-media`, the share of boost intervals holding a demotion and each periodic task's job miss rate by the records (`harness/tools/records.py`; a job late past its period, or skipped, as `harness/tools/harness/aggregates.py` counts it). For the editors of `c7-office`, `c7-browsing`, `c1-mail` and `c7-dev`, their demotions.

## Results

The edges (`edges.md`, means; medians beside):

| task | CPU per 100 ms boost interval |
|---|---|
| music player (`c1-media`) | 710 µs (694) |
| frame chain, gaming base (`c1-gaming`), 17 tasks | 1 716 to 8 616 µs |
| frame chain, C2 pair (`c2-p2a`), 17 tasks | 1 633 to 12 729 µs |
| video player (`c1-media`) | 12 089 µs (11 976) |
| call (`c1-meeting`) | 23 867 µs (22 659) |

At the primary 10 000 µs (`table.md`): the call demoted in 0.98 of its boost intervals, the video player in 0.89, no gaming-base chain task, three `c2-p2a` chain tasks in at least half of theirs. On the counterparts (`fixed-check.md`): the call demoted in 0.97 and missing 527 of its 2 639 jobs (0.200, 190 of them skipped); the video player demoted in 0.88, neither player missing a job. The editors: the office writer demoted in 0.05 of its boost intervals on `c7-office` (13 demotions), the browser in 0.06 on `c7-browsing` (21), the mail client in 0.04 on `c1-mail` (55), VS Code in 0.35 on `c7-dev` (182).
