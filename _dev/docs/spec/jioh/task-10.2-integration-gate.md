# Task 10.2 — The integration gate

Sub-task 10.2 of Phase 10 (`_dev/docs/spec/jioh/phase-10-integration-and-the-rq0-run.md`, decision 4), decided on 2026-11-14: what the simulator and the daemon must show before the RQ0 run may start, on which binary, and what binds the run to the programs that showed it. The conformance items are the ten of the RQ0 gate spec's `simulator-conformance` statement (`harness/experiments/rq0-gate.yaml`).

## Scope

- `simulator/src/sim.cpp` compiled on the home machine, and the runner's machine configuration on that binary and on `daemon/daemon.py`.
- The hand fixtures under `harness/tools/tests/fixtures/` that carry a trace — the seven hand pairs (`mock-office`, `mock-media`, `mock-p1a`, `mock-chain`, `mock-guards`, `mock-switch`, `mock-wakes`) and the two reference fixtures (`fix-object`, `fix-tree`) — replayed through that binary. `mock-scores`, `mock-grades` and `mock-experiment` carry no trace and are outside the gate.
- Black-box unit tests on that binary for the conformance items the fixtures do not show.
- `daemon/daemon.py` compared with the harness's mock daemon on the RQ0 run's own run list.
- The simulator's and the daemon's version strings pinned in the RQ0 gate spec and checked by the runner.
- The RQ0 gate spec's edit at the gate's pass, with one harness changelog entry and one re-pin.

## Locked decisions

### 1. The cap is null in three fixtures

`mock-guards`, `mock-p1a` and `mock-switch` are replayed with every `batch_bandwidth_cap` null (decided 2026-11-13, `simulator/memo/memo_261111.md` Part K2).

### 2. When a fixture matches

A fixture matches when every µs holds the same lines in any order and the records the harness builds from the simulator's trace equal the fixture's `expected.csv` (decided 2026-11-13, Part K2). The header line is left out of every comparison. `x_`-prefixed lines are left out on both sides (data contracts §9: the harness ignores the prefix).

### 3. Records are equal in every column but two

The records equal `expected.csv` when every column but `sim` and `source_sha256` is equal, row for row. `fix-object` and `fix-tree` have no `expected.csv`; for them the match is the line comparison against the reference trace.

### 4. The replay runs through `simulator/src/sim` with the invocation contract's flags

The replay calls `simulator/src/sim` with `--workload`, `--schedule` and `--out-trace`; the replay tool keeps the positional form for ladder rungs. Each fixture is replayed twice and the two traces are byte-identical. Each trace's header `sim` equals the version string `simulator/src/Makefile` prints. The refusal cases of the invocation contract (item (h) of the conformance statement) are a committed unit test.

### 5. The schedule of a fixture without a `config-schedule.json`

For `mock-office`, `mock-wakes`, `mock-media` and `mock-chain` the schedule is rebuilt from the fixture's own `config_applied` lines, one entry per line at the line's time, with the boot parameters read from `harness/boot-defaults/ostep.json`. Their records are built as the fixture's own test builds them, with no schedule passed to the builder.

### 6. Three items are shown by unit tests on the gated binary

The cap as a work-conserving ceiling on the behavioural batch class (item (d)), the strict idle class (item (e)) and the frame chain's woken stages in EDF's deadline class (item (f)) are shown by black-box unit tests on the gated binary, beside the simulator's existing unit tests. The gate is the fixture replay plus those tests. The `simulator-conformance` statement is restated at the pass to say which item is shown where.

### 7. The reference fixtures' readings are assertions

What the two `worked.md` files read off `fix-object` and `fix-tree` — the held wake taken at the spawn-table child's birth (item (i)), the children wait completing at the last child's `task_end` (item (g)), every arrival matched by a `task_end` — is asserted by a black-box unit test on the gated binary. The line comparison against the reference traces stays.

### 8. Each behavioural unit test is shown to fail

Each of the four behavioural tests — the strict idle class, the frame chain in EDF's deadline class, the spawn-table wake, the children wait — is shown to fail on a simulator without the behaviour, the ladder rung before the item's stage or a mutant of the current source, and the failure is recorded with the gate's results. Each test asserts its item as the conformance statement words it, the strict idle class under all four algorithms.

### 9. The daemon is compared with the mock daemon on the run's own list

`daemon/daemon.py` and the harness's mock daemon are both run on the exact run list the runner expands from the RQ0 gate spec, and every schedule and log is compared byte for byte. The count is recorded with the gate's results.

### 10. The daemon's version string

The runner's machine configuration names the daemon as `daemon@<12 hex>`, the git blob hash of the source bytes the daemon runs — `daemon/daemon.py` and the `drivertable` module it imports — printed by a `version` target in `daemon/Makefile`.

### 11. The gate spec pins both version strings

The RQ0 gate spec gains two pins, the simulator's and the daemon's version strings. The runner checks them against the machine configuration before any run and refuses on a mismatch. The pins are optional in the experiment schema: the mocks' specs and the generated smoke spec run without them. The machine configuration stays uncommitted.

### 12. A short attended run through the runner

The smoke tool runs on the real machine configuration over seven files — `c1-photo`, `c1-office`, `c7-mail`, `c2-p2b`, `c1-gaming`, `c7-compile`, `c1-compile` — in runs and cache directories of its own, so the cold smoke of 10.3 keeps an empty cache.

### 13. One entry point, parts that run alone

The gate has four parts: the simulator's unit tests, the fixture replay, the daemon comparison, the short runner run. One entry point runs them, and each part runs alone, tied to the version string it checked. A change to the simulator's source reruns the unit tests, the fixture replay and the short runner run; a change to the daemon's source reruns the daemon comparison and the short runner run. The gate is passed when every part has passed on the two version strings the gate spec pins.

### 14. On a failure 인지오 changes the faulty side

The ratified contract decides which side is wrong, and 인지오 makes the change. A simulator fault is fixed as a new stage on the step ladder, ported to `simulator/src/sim.cpp`, and reported to 인경민 by memo. A fixture or test fault is corrected with a harness changelog entry. Where the daemon and the mock daemon differ, the wrong program is changed, a change to `daemon/daemon.py` reported to 박이안 by memo, and the comparison rerun on the new version string. The Phase 10 spec's decision 4 is restated to match.

### 15. What the pass writes

- The RQ0 gate spec's edit, with one harness changelog entry and one re-pin: the `simulator-conformance` statement restated (decision 6), the two version pins (decision 11), and the four driver tables' citation `simulator/src/sim.cpp:328–366` restated to `struct Lottery` by name (decided 2026-11-13, Part K3).
- Each part's output under `_dev/research/jioh/`, with the compiler's version and the binary's SHA-256.
- One memo to 인경민: what was added to the simulator tree, the gate's result, the pinned version. A memo to 박이안 only if `daemon/daemon.py` itself changed.

## Invariants

- The full run does not start until every conformance item is shown on the binary that runs it (Phase 10 spec); decision 11 makes it the runner's refusal.
- A source change to either program after the pass changes its version string: the run cannot start until the parts of decision 13 are rerun and the pins restated by a harness changelog entry.

## Open items

Left to the implementation plan: where the entry point lives; each unit test's workload, assertions and control; how the daemon comparison is spread across cores; how the machine configuration is written on the home machine.
