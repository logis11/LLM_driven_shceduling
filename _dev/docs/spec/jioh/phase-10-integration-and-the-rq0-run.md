# Phase 10 — Integration and the RQ0 run

인지오's Phase 10 in `_dev/TODO.md`, decided on 2026-11-01: the harness run on the real simulator and the real daemon, through the RQ0 gate spec's verdict (`harness/experiments/rq0-gate.yaml`). Phase 9 ended with the project ready for this run; the simulator's owed conformance items are handed to 인경민 in `docs/memos/2026-10-30-harness-changes-for-the-simulator.md`.

## Scope

- The RQ0 gate spec's two remaining pre-run lines: link 2's falsification condition (`docs/research-claims.md`, the chain's link 2: some of the differences are invisible to behavioural observation) and the cap band line (the verdict count beside the primary under other `batch_bandwidth_cap` values).
- The runner's machine configuration moved from the mocks to the real simulator and the real daemon, and the simulator's conformance shown on the harness's hand fixtures.
- A cold smoke on the real programs and, from its figures, the response to the full run's cost.
- The RQ0 run, its verdict and its record.
- The docs that describe the harness and the mocks brought to the phase's end state.

Out of scope: the failure procedure the RQ0 gate spec names on a FAIL (its configuration search and what follows), the RQ1–RQ4 experiment specs, the hold-time plan's step 0 (`_dev/docs/plan/jioh/hold-time-and-hysteresis.md`, the need measured with no rule), and the Layer 1 and RQ4 items the experiment specs carry.

## Locked decisions

### 1. The phase ends at the verdict

Phase 10 closes when the RQ0 verdict — PASS or FAIL, read as the RQ0 gate spec pre-registers it — is reached and recorded. On a FAIL the gate spec's failure procedure is a later phase.

### 2. The phase opens now

Phase 10 opens on 2026-11-01. The work that needs no simulator — the gate spec's pre-run lines — comes first; the integration waits for 인경민's owed items (the two mailboxes and `wake_drop`, the zero-wait `ready` line of a FORK taking a free slot, the drain at a RUN's end, `WAIT children:<id>`, the trace header's version string); the smoke, the run and the verdict follow.

### 3. The run uses the real daemon

The RQ0 run runs `daemon/daemon.py`, the committed daemon, in the mock daemon's place. No further daemon work is a prerequisite of this phase; the daemon's ownership is settled outside it.

### 4. The integration gate is shown by 인지오 on the harness's hand fixtures

인지오 compiles `simulator/src/sim.cpp` on the home machine and replays every hand fixture under `harness/tools/tests/fixtures/` through that binary, each trace compared line by line with the fixture's. A fixture that differs goes back to 인경민. The gate is passed when every fixture matches, and that binary runs RQ0. What 인경민 checks on the simulator's own step ladder is 인경민's development, not the gate.

### 5. A cold smoke, then the cost response, then the full run

After the gate the real programs run the smoke with an empty cache, and its wall time per file, `c6-dual`'s among it, is recorded. From those figures the full run's cost is projected and one response is chosen — a cheaper records path, N changed under the RQ0 gate spec's `n-grounding` statement, or the cost carried — by a harness changelog entry before the run. The machine is the home M1 Pro; the full run's budget is about 80 hours of unattended wall time, the leave two weeks on.

### 6. The gate spec's two pre-run lines are one sub-task

Link 2's falsification condition and the cap band line are fixed in the RQ0 gate spec in one sub-task, with one harness changelog entry and one re-pin. The two pre-run items already in place — the trace-replay check (the `trace_replay` line: its four files, its agreement criterion and what a disagreement leads to) and the TIMER docs restated to the skip rule — are marked done.

### 7. The hold-time plan's step 0 stays in the Backlog

The need measured with no rule — the flap-stress set and the C4 files under `oracle` and `random` on the real programs — is not part of Phase 10. It runs on the integrated pipeline after the phase closes, as the Backlog states.

### 8. Exit criteria

At the phase's end: the verdict read from the report after every guard; the report (`report.json` and its rendering) committed to the repository; a record of the run under `docs/` — its dates, machine, cost, N and the changelog entries behind it, the verdict and the reporting lines; `docs/research-claims.md`'s link 1 line restated to the outcome; the TODO closed. The report's place in the repository is decided in the run sub-task's own spec session.

### 9. Structure of the phase

Five sub-tasks, in order: the gate spec's pre-run lines (10.1); the integration gate (10.2); the cold smoke and the cost response (10.3); the RQ0 run, its verdict and its record (10.4); the docs sweep (10.5) — the harness guide's conformance passages, the mocks' README, the docs index, the TODO. The Layer 1 and RQ4 item of the old Phase 10 list moves to the Backlog, carried by the experiment specs its text names. Schedule: 10.1 and 10.2 before the next weekend; 10.3's smoke left running over the overnight leave that weekend, its cost response decided in the week after; 10.4 over the leave two weeks on; 10.5 after.

### 10. The smoke does not wait for the gate

If 인경민's owed items are not done by the overnight leave, the cold smoke runs then on the simulator as committed, compiled on the home machine, for its cost figures. The integration gate completes before the full run; the full run never starts without it. Whether the smoke is rerun on the gated binary is decided on the smoke's figures.

## Invariants

- The full run does not start until every conformance item of the RQ0 gate spec is shown on the binary that runs it (decision 4).
- Nothing in the run changes after execution begins except by a harness changelog entry made before any run (the RQ0 gate spec's own rule); the cost response of decision 5 is such an entry.

## Open items

Left to each sub-task's own spec session: the cost response's choice and its figures (10.3); the report's place in the repository (10.4).
