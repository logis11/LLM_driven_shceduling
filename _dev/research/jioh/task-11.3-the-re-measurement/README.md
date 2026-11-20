# The re-measurement (11.3)

The record of sub-task 11.3 (`_dev/docs/spec/jioh/task-11.3-the-re-measurement.md`). The paths in the files are relative to the repository root; each script runs from there. The dataset tools run on Python 3.12, the interpreter holding `jsonschema_rs` (`dataset/tools/requirements.txt`).

| file | what it holds |
|---|---|
| `as_run.sh` | decisions 2, 4 and 11: the RQ0 run's programs — the harness and the simulator's source at the run's commit, `6086e7e1` — extracted into `as-run/` (local only) and the simulator built there, `simulator@0d323c84470a`; the harness there scores with the scorer as run, before 11.1's sign rule |
| `finding_builds.py`, `finding-builds.json` | decisions 1, 2 and 14: `c7-ml-train` compiled from a copy of the library with one of its four carried values at the lower bound of its interval, one build per value, and the two controls — nothing moved, all four moved; the library copies and the builds under `finding/` (local only), their SHA-256 and the controls' bytes against the blessed artifacts in the JSON. Each build carries the id of the file it stands for: the four and the build with nothing moved `c7-ml-train`, the build with all four moved `c7-ml-train@corner-low` |
| `spec_copy.py` | decisions 2, 11 and 12: a throwaway copy of the RQ0 gate spec holding the criterion's runs on the files named, the simulator pinned to the version named, and the machine configuration naming that simulator and the build directory; linted by the harness the runs use, written under `runs/`, never committed |
| `finding_run.sh` | decisions 2 and 4: one spec copy per build directory, the controls first, each run on the RQ0 run's programs; outputs under `runs/rq0-gate-finding-<dir>/` |
| `finding-first-run.json` | the finding step's first run, every build under an id of its own (`c7-ml-train@<build>`): the control with all four moved did not reproduce the RQ0 run — 16 of its 100 `random` runs' P99 differed, every score and the gap equal, the schedules identical but the id. The simulator seeds its lottery draw from the FNV-1a hash of the workload id (`simulator/src/sim.cpp`, `lottery.seed(fnv1a(sim.workload_id()))`; the interpretation contract's §1), so a run under a LOTTERY row draws other tickets under another id. The builds of that run were never read; its outputs deleted |
| `finding_read.py`, `finding.json` | decisions 2 and 3: the controls' score rows and gap rows against the RQ0 run's, then each build's `fixed` and `oracle` P99 and its gap under the scorer as run, and the builds below g |

| `closing_run.sh`, `closing_read.py`, `closing.json` | decisions 11 and 12: the three judging files holding `python3` rebuilt on the second bless, the criterion's 102 runs each beside `c2-p1b`, once on the RQ0 run's programs under the scorer as run (`runs/rq0-gate-11-3-closing/`) and once on the fixed programs (`runs/rq0-gate-11-3-current/`); the count at the re-measured value, the other sixteen judging files' rows carried from the RQ0 run and from 11.2's rerun |
| `runs/<experiment>/` | decision 14: the aggregates, scores and report of the finding step's five experiments and the closing, gzipped (`-9 -n`); their traces deleted |
| `campaign/method.md` | decisions 5 to 7: the training run's fresh campaign — the original campaign's method, the tag, the count, the launch, the replacements, the differences the venue forces; its amendments: the stop and the probe |
| `campaign/watch_loop.sh`, `campaign/probe_read.py` | the campaign's watch, restarted after each landing; the probe's reading — each repeat's blocks and what ended them, against the criterion |
| `bless_report.py`, `bless-report.json` | decision 10: the second bless's report — over every manifest under `dataset/`, the artifacts changing beyond the library's hash against the first bless and the demands that move |
| `campaign/results/` | the campaign at 107: the pooled record and its rendering, `pool_runs.py`'s output, every repeat's blocks and what ended them (`blocks-check.json`, `campaign/blocks_check.py`), the runs and draws |
| `campaign/probe-2026-11-20/`, `campaign/fold-check.json` | the probe: the two landed repeats' pooled record, raw and with the fold, their reading (`probe.json`), the runs and draws; the fold checked on the original campaign's six repeats and the probe's two |
| `campaign/stop-2026-11-20/` | the stop: the two landed repeats' pooled record and rendering, the runs and the draws |

**The controls** (2026-11-20): the build with nothing moved, as `c7-ml-train`, and the build with all four moved, as `c7-ml-train@corner-low`, each byte-identical to its blessed artifact; on the RQ0 run's programs each reproduces the RQ0 run's 204 score rows and its gap row in every field.

**The finding** (2026-11-20), the editor's input latency P99 at the primary boot default under the primary table, the gap under the scorer as run at the 1,000 µs floor:

| build | `fixed` P99 (µs) | `oracle` P99 (µs) | gap |
|---|---|---|---|
| nothing moved | 7,194,480.40 | 8,020,875.92 | 2.512497 |
| `code-editor`'s `utility/libuv-worker` gap table at −5.63 % | 7,194,480.40 | 8,020,866.04 | 2.496021 |
| `code-editor`'s `utility/libuv-worker` run table at −2.36 % | 7,194,480.40 | 8,020,875.92 | 2.509309 |
| `cpu-batch`'s `python3` runs between voluntary blocks at −27.3 % | 8,020,850.48 | 8,020,875.92 | 0.000000 |
| `cpu-batch`'s `python3` block per run at −10.8 % | 7,194,480.40 | 8,020,875.92 | 2.505678 |
| all four moved | 8,020,840.08 | 8,020,865.52 | 0.000000 |

The training run's runs between voluntary blocks moves the file across g alone: `fixed` and `oracle` within 25.44 µs, under the floor, the term no headroom. The entry found is `cpu-batch`'s `python3`, re-measured at 107 repeats (decision 5).

**The closing** (2026-11-21), on the RQ0 run's programs under the scorer as run: `c2-p1a` 0.377 → 0.417, `c1-ml-train` 0.610 → 0.527, `c7-ml-train` 2.512 → 0.000 (`fixed` 8,020,850.48 µs, `oracle` 8,020,875.92, no headroom); every guard passes, no wait past 30 s. With the other sixteen judging files' rows the RQ0 run's, 5 of 19 meet g against K = 10: fail, final. On the fixed programs, the post hoc reading at the re-measured value: 4 of 19, `c1-ml-train` 0.468 → 0.390.
