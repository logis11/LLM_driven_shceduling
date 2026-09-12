# tools

All of the harness's code: the `harness` Python package, one command-line tool per stage, the tests, and the two mocks that stand in for the daemon and the simulator until the real programs land. Python 3.12; dependencies in `requirements.txt`. Every command runs from the `harness/` directory and takes named flags only.

## The commands, in pipeline order

| command | in → out | exit codes |
|---|---|---|
| `records.py` | one (run file, trace) pair, plus the config schedule → one records CSV; guard messages on stderr | 0 |
| `score.py` | records CSVs or directories of them → an aggregates CSV and a scores CSV | 0 |
| `guards.py` | a run-set manifest and the aggregates CSV → the guards CSV | 2 if any guard failed |
| `grade.py` | a manifest of recognition logs with ground truth and the driver table → one recognition records CSV per run and the grades CSV | 2 if the oracle was not perfect on a graded point |
| `evaluate.py` | a per-experiment spec and the four files above → `report.json` and `report.md` | 0 pass, 2 fail or invalid, 1 refusal |
| `run.py` | a per-experiment spec and a machine configuration → every run invoked, every stage above, the report | 1 a failed run, else the verdict's |
| `smoke.py` | a generated throwaway spec over the compiled coreset, run through `run.py`'s path with the mocks | 0 once a report is written |

And three lints plus one checker that is not part of the harness:

| command | checks |
|---|---|
| `lint.py` | every fixture pair under the frozen contracts, its expected files against the schemas, every boot-default file against its schema |
| `scoring_lint.py` | the scoring spec against its schema, the compiled coreset, and the dataset's recipes |
| `guards_lint.py` | the guard spec against its schema, the code's guard registry, and the C2 pair recipe |
| `experiment_lint.py` | every per-experiment spec against its schema, the build, the pinned scoring spec's terms, the registries, and its pins |
| `check_mlfq_levels.py` | the `x_mlfq_level` trace lines the readers skip, against each switch window; a diagnostic for the simulator, not a harness stage |

`--help` on any command prints its flags. `make lint`, `make test`, and `make smoke` in the parent directory run the lints, the suite, and the smoke.

## Layout

- `harness/` — the package the commands and the runner call. [harness/README.md](harness/README.md) explains how the modules fit together.
- `tests/` — the pytest suite, the hand-written fixtures with their expected outputs, and the mocks. [tests/README.md](tests/README.md).

## Conventions the code keeps

- The harness never imports the daemon's or the dataset's modules. Where it must reproduce their logic, a test pins the two: the driver-table composition against the daemon's, the OSTEP boot default against the config schema's defaults.
- Numbers are integers or exact fractions until they are formatted for a file, and files carry decimal strings, never floats. Two runs of the same input produce byte-identical files.
- Every judgement is data: the scoring spec, the guard spec, and the per-experiment spec. A constant in code is a bug.
