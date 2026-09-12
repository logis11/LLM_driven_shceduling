# harness

The experiment harness turns what the simulator and the daemon leave behind into the numbers the paper reports, and into one verdict for RQ0. It never schedules anything and never recognizes anything: it reads a trace and a recognition log, measures, scores against a frozen scoring spec, checks the run with frozen guards, and judges against a pre-registered experiment spec.

```
                daemon ──► config schedule + recognition log ──┐
workload ──►                                                   ├──► harness ──► report
                simulator ─────────► trace ────────────────────┘
```

Inside the harness the flow is one direction, one file per stage, every file long-format CSV or JSON with a schema beside it:

```
(run file, trace, schedule) ──► records ──► aggregates ──► scores ──┐
                                   │                                 ├──► RQ0 gate evaluator ──► report.json + report.md
                                   ├──► guards ──────────────────────┤
recognition log + ground truth ──► grades ───────────────────────────┘
```

## Reading order

If you are new, read `docs/background-guide.md`, then `docs/harness/harness-and-records-guide.md` (Korean, worked examples), then `docs/harness/metrics.md`, which defines every number. Each folder below has its own README that says what it is for and how its files are produced and read.

| folder | what lives there | README |
|---|---|---|
| `records/` | the schema of the records file, the harness's first product: one raw observation per row | [records/README.md](records/README.md) |
| `aggregates/` | the schema of the aggregates file: every aggregate of a run, whether scored or not | [aggregates/README.md](aggregates/README.md) |
| `scores/` | the schema of the scores file: per-term shares and per-file scores against the fixed baseline | [scores/README.md](scores/README.md) |
| `scoring/` | the scoring spec, frozen: which terms value each coreset file, with what weight | [scoring/README.md](scoring/README.md) |
| `guards/` | the guard spec, frozen, and the schema of the guards file: the checks a run must pass before its numbers are read | [guards/README.md](guards/README.md) |
| `grades/` | the schema of the grades file: Layer-1 recognition accuracy, pooled | [grades/README.md](grades/README.md) |
| `boot-defaults/` | the boot-default configurations the runner hands the daemon: the primary and the sweep | [boot-defaults/README.md](boot-defaults/README.md) |
| `experiments/` | the per-experiment specs and the report schema; `rq0-gate.yaml` is the RQ0 gate spec | [experiments/README.md](experiments/README.md) |
| `tools/` | the code: the `harness` package, the command-line tools, the tests, the mocks | [tools/README.md](tools/README.md) |

Beside the folders: `CHANGELOG.md`, the harness tree's own changelog, where the scoring spec and the guard spec were frozen on 2026-09-12 and every later change to a committed data file or a program is recorded; `Makefile`, the three targets below; `runner.example.yaml`, the machine configuration that drives the mocks.

## Running it

Everything runs from this directory with Python 3.12 and `tools/requirements.txt`. The scoring lint and the experiment lint read the compiled coreset, so build the dataset once first.

```
pip install -r tools/requirements.txt -r ../dataset/tools/requirements.txt
make -C ../dataset dataset        # compiles dataset/build/coreset-single
make lint                         # fixtures, scoring spec, guard spec, experiment specs, boot defaults
make test                         # the suite, about 90 s
make smoke                        # the whole pipeline on the mocks over every scored coreset file, 5–8 min
```

`make smoke` generates a throwaway experiment spec over the files as they are, runs it through the runner with the mock daemon and mock simulator, writes everything under `runs/`, and discards the spec. To run a real experiment, copy `runner.example.yaml` to `runner.yaml` (git-ignored), point it at the real programs, and run:

```
python3 tools/run.py --spec experiments/rq0-gate.yaml --machine runner.yaml
```

The runner invokes each program twice per run and requires byte-identical outputs, caches every invocation, and stops before scoring if any run fails. The report lands at `runs/<experiment>/report.json` with a Markdown rendering beside it. Exit codes: 0 pass, 2 fail or invalid, 1 a failed run or a refusal.

Every stage is also its own command, so a single pair can be inspected by hand:

```
python3 tools/records.py --run RUN.json --trace TRACE.jsonl --schedule SCHEDULE.json --out records.csv
python3 tools/score.py --records records.csv --out-aggregates aggregates.csv --out-scores scores.csv
python3 tools/guards.py --manifest guards-manifest.json --out guards.csv
python3 tools/grade.py --manifest grade-manifest.json --out-grades grades.csv
python3 tools/evaluate.py --spec experiments/rq0-gate.yaml --aggregates … --scores … --guards … --grades … --out-report report.json --out-render report.md
```

## What is frozen, and what changes how

Three files are data the code obeys and never a constant in code: the scoring spec, the guard spec, and the per-experiment spec. The first two are frozen; the RQ0 gate spec pins their bytes by SHA-256 along with the prior driver table and the dataset build manifest, and the evaluator refuses to judge if any pin no longer matches. A change to a frozen file is an entry in `CHANGELOG.md` made before any run reads it, and a new pin. The reasons behind every number in the RQ0 gate spec are written in that file, beside the number.

CI runs `make lint` and `make test` on every push (`.github/workflows/harness.yml`) and the smoke on `main`, on demand, and on pull requests that touch the harness, the dataset, or the driver table (`harness-smoke.yml`).

## Where the definitions are

- `docs/harness/metrics.md` — every primitive, aggregate, normalisation rule, floor, and constant, with its source.
- `docs/data-contracts.md` — the input formats (§9 trace, §4 run file, §7 config schedule, §8 recognition log, §10 driver table) and the invocation contract (§11).
- `_dev/docs/spec/jioh/` — the decision records behind each module, by sub-task.

This tree is 인지오's.
