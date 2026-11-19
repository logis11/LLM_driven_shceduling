# The degraded oracle (11.2)

The record of sub-task 11.2 (`_dev/docs/spec/jioh/task-11.2-the-degraded-oracle.md`). The paths in the files are relative to the repository root; each script runs from there.

| file | what it holds |
|---|---|
| `cases.md` | decision 8's case table: one row per case — the file, the term, the combination, the class, the evidence, the fixing commit — and each case's reading, its counterfactual's prediction recorded before the run |
| `cap_check.py`, `cap-check-<file>.json` | one run's trace read against the batch-class rule and the cap — every park on a batch-class task while a non-batch task is runnable, no parked task running, the batch class's CPU while capped within the cap and the bucket's depth — and the scored task's `input_latency` rows (the metrics doc's §6.12) or `app_latency` rows (§6.13) recomputed against the run's records |
| `counterfactual.py` | a counterfactual run: an RQ0 run's config schedule with a knob moved, on the pinned simulator, its records and aggregates built as the runner builds them, the case's term beside the scored oracle value and the trace's hash beside the base run's |
| `counterfactual/<file>/<name>/` | each counterfactual run — `schedule.json`, `aggregates.csv`, `result.json` (the simulator's version and the trace's hash), and its `cap-check.json` where the cap is read; `trace.jsonl.gz` and `records.csv.gz` local only (`.gitignore`), reproducible from the schedule on that simulator. `replay` is the base schedule with nothing moved, reproducing the run's trace hash. From `c1-render` on, the runs are on the RQ0 run's simulator rebuilt from its source (`simulator@0d323c84470a`, `git show 586e41ce~1:simulator/src/sim.cpp` and `mini_json.hpp`, the flags of `simulator/src/Makefile`); `c7-dev`'s and `c7-video-edit`'s on the pinned build before stage AF |
| `run_profile.py` | a run's shape from its trace beside another run of the same file: CPU per task inside the window, each task's bursts between voluntary blocks, where the cap's parks fall |
| `stage_regression.py`, `stage-regression-<stage>.json` | a simulator stage against the RQ0 run's own traces: every file under its fixed and oracle schedules run again on the binary, the trace read line by line against the run's with the header (the version) left out |
| `elsewhere/cap-check-<file>-<run>.json` | `cap_check.py` on the runs of the cases read at other combinations: the oracle run, and the fixed run at the combination's boot default |
