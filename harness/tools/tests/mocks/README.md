# mocks

Two test doubles that speak the invocation contract (`docs/data-contracts.md` §11) so the whole harness can run before the real daemon and the real simulator speak it: no daemon program is in the repository yet, and the reference simulator (`simulator/src/sim.cpp`) takes its two inputs positionally and prints the trace to standard output. Both live in the test tree on purpose, and Phase 10 (integration and the RQ0 run) swaps them for the real programs. Nothing here belongs in the daemon or simulator trees.

## The mock daemon

`daemon.py` is the library; `mock_daemon.py` the command:

```
python3 mock_daemon.py --workload W.json --condition fixed|oracle|random \
        --telemetry focus|names --driver-table TABLE.yaml --boot-default BOOT.json \
        --out-schedule SCHEDULE.json --out-log LOG.json [--seed N]
```

It is faithful for the three conditions RQ0 needs. It extracts the visible projection from the workload, walks its pinned events under the six telemetry rules to find the query points, shows each snapshot in the telemetry shape its `--telemetry` flag names, answers each from ground truth (`oracle`), from a seeded uniform draw over the driver table's rows (`random`), or not at all (`fixed`), and writes a contract-valid config schedule and recognition log. Where the oracle's answer is undefined, an `ambiguous` segment or the terminal snapshot, the query carries `fallback` and the schedule entry repeats the boot default. It emits `unmodified` only: no validator, no clamping, no `held`, no LLM path. A test pins its query points and graded set on the core set to the counts of the current blessed set (the 8.4 spec measured them first, on the core set of 2026-09-11).

## The mock simulator

`simulator.py` is the library; `mock_simulator.py` the command:

```
python3 mock_simulator.py [--replay TRACE.jsonl] --workload W.json --schedule SCHEDULE.json --out-trace TRACE.jsonl
```

The generator emits a contract-valid trace for any workload and schedule from one rule that models no scheduling: at every stimulus the stimulated task becomes ready, runs for exactly 1 µs, and ends its run. A task whose first instruction is a WAIT, a spawned child included, blocks in its arrival step as the reference simulator's does unless a wake is already stored for it: with none, its arrival writes no `ready` line and no run, and it first runs at the wake that completes that WAIT; with one, the WAIT completes on it and its arrival is `ready(arrive)` with its run. A wake sent to a task before its arrival is stored for it, whatever its channel, and taken in the arrival step: its `ready(wake)` line, the zero-wait line of the WAIT it completes (`docs/harness/metrics.md` §11, item 1), is written at the arrival beside `ready(arrive)`, never before it. That is enough for every coreset file to flow through the whole pipeline, and it is deliberately not enough to show a scheduling effect: on the mocks, `fixed`, `oracle`, and `random` score the same, every judging file reads as no headroom, and the C2 pair guard fails under `oracle`. Those are the expected results of a simulator that never models a queue, not defects.

The replay copies a hand-written fixture trace after checking that it belongs to the workload named. The runner uses it, through `--replay` in the command prefix, to run the fixtures whose values were computed by hand through the same path as everything else.

## Why they matter

Both programs are the first implementations of the invocation contract. When 인경민's simulator and 박이안's daemon are run in their place, the runner's machine configuration changes and nothing else does.
