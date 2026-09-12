# mocks

Two test doubles that speak the invocation contract (`docs/data-contracts.md` §11) so the whole harness can run before the real daemon and the real simulator exist. Both live in the test tree on purpose and are discarded in Phase 9. Nothing here belongs in the daemon or simulator trees.

## The mock daemon

`daemon.py` is the library; `mock_daemon.py` the command:

```
python3 mock_daemon.py --workload W.json --condition fixed|oracle|random \
        --driver-table TABLE.yaml --boot-default BOOT.json \
        --out-schedule SCHEDULE.json --out-log LOG.json [--seed N]
```

It is faithful for the three conditions RQ0 needs. It extracts the visible projection from the workload, walks its pinned events under the five telemetry rules to find the query points, answers each from ground truth (`oracle`), from a seeded uniform draw over the driver table's rows (`random`), or not at all (`fixed`), and writes a contract-valid config schedule and recognition log. Where the oracle's answer is undefined, an `ambiguous` segment or the terminal snapshot, the query carries `fallback` and the schedule entry repeats the boot default. It emits `unmodified` only: no validator, no clamping, no `held`, no LLM path. A test pins its graded set on the coreset to the counts the 8.4 spec measured.

## The mock simulator

`simulator.py` is the library; `mock_simulator.py` the command:

```
python3 mock_simulator.py [--replay TRACE.jsonl] --workload W.json --schedule SCHEDULE.json --out-trace TRACE.jsonl
```

The generator emits a contract-valid trace for any workload and schedule from one rule that models no scheduling: at every stimulus the stimulated task becomes ready, runs for exactly 1 µs, and ends its run. That is enough for every coreset file to flow through the whole pipeline, and it is deliberately not enough to show a scheduling effect: on the mocks, `fixed`, `oracle`, and `random` score the same, every judging file reads as no headroom, and the C2 pair guard fails under `oracle`. Those are the expected results of a simulator that never models a queue, not defects.

The replay copies a hand-written fixture trace after checking that it belongs to the workload named. The runner uses it, through `--replay` in the command prefix, to run the fixtures whose values were computed by hand through the same path as everything else.

## Why they matter

Both programs are the first implementations of the invocation contract. When 인경민's simulator and 박이안's daemon are run in their place, the runner's machine configuration changes and nothing else does.
