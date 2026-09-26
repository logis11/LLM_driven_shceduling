# src/sim.cpp — build notes and conformance audit

> Working notes for the reference simulator in this directory. Records what `sim.cpp`
> currently implements, how it was verified, and where it stands against the repo's
> contract documents. Not a normative spec — the contracts under `docs/` win.

## 1. What this is

`sim.cpp` is a one-lane discrete-event scheduler simulator: a pure function
`(workload.json, config-schedule.json?) → JSONL trace`. It was carried from an
earlier snapshot (stage I: core + MLFQ + preemption + gen, with a hardcoded `main`
and no loader) up to **stage R** (full instruction set, workload loader, config
schedule with policy handoff), matching the one-rung-at-a-time ladder in `../notes/`.

Build:
```
g++ -std=c++17 -O2 -Wall -Wextra -o sim sim.cpp
./sim <workload.json> [<config-schedule.json>]      # trace → stdout (JSONL)
```
`sim.cpp` depends on `mini_json.hpp` (in this directory).

## 2. Stages implemented (A–R)

| stage | feature |
|---|---|
| A–I | clock + event queue, Instr/Task/step, lane + dispatch, WAIT + wake, depart, timeslice + preemption + `gen`, Policy interface, Trace/Clock seam, MLFQ rules 1–5 (boost via `Clock::arm`) |
| J | `SLEEP` — relative wake (`now + N`) |
| K | `TIMER` + backlog — absolute grid (`t0 + k·P`), missed ticks consumed immediately |
| L | `LOOP` flattening — `LOOP_BEGIN/END` + back-jump; unbounded and bounded counts |
| M | channels + `WAKE` + mailbox — wake is channel-addressed; a wake with no waiter goes to a mailbox (never lost) |
| N | `FORK` / `spawn_table` / `fork_cap` — children born at runtime; `tasks_` is a `std::deque` so a grow does not dangle a held `Task&` |
| O | JSONL trace — 7 runtime events + `meta` header (data-contracts §9) |
| P | `deadline` events — one per periodic job, `due`/`met`/`slack_us` |
| Q | workload loader — `mini_json.hpp`, 2-pass forward-reference resolution, whole-file rejection on any violation |
| R | config schedule + `handoff()` — mid-run policy switch (e.g. MLFQ→FIFO→MLFQ) |

## 3. Verification performed

Golden reference: `../notes/sim_r.cpp` (the ladder's final rung), compiled and run
on the same inputs. Comparison normalizes only the `meta.sim` field
(`"src/sim"` vs `"notes/sim"`), the sole intentional difference.

- **All 24 coreset workloads** (`dataset/build/coreset-single/*.workload.json`) →
  **byte-identical** trace to `sim_r`, up to 1,522,416 lines (`c6-dual`).
- **Config-schedule path** — a real coreset workload run under a hand-written
  MLFQ→FIFO→MLFQ schedule → byte-identical to `sim_r`; 3 `config_applied` events,
  handoff exercised.
- **Determinism (non-negotiable 4)** — same input run twice → byte-identical
  (`c1-office`, `c1-compile`, `c1-gaming`).
- **Feature paths actually exercised** (not dead code): FORK (`c1-compile` spawns
  100 children, `report()` confirms), deadline (`c1-gaming` emits 4,482),
  MLFQ demote/boost, all five `ready` causes.
- Compiles clean under `-Wall -Wextra`.

## 4. Conformance audit against the contract docs

Checked against `docs/simulator/simulator-guide.md` (normative),
`docs/simulator/interpretation-contract.md` (normative), `docs/data-contracts.md §9`,
`dataset/schema/workload.schema.json`, and `docs/harness/metrics.md`. This audit is
independent of the `sim_r` comparison.

### Conforms (verified against the docs)

- **Non-negotiables (guide §2), all 7**: two inputs only; one lane; integer µs (no
  float in time arithmetic); zero runtime randomness / byte-identical reruns;
  `ground_truth` never reaches the core (loader reads `meta.id` + `events` only);
  the trace keys on `id` (`sid`), scheduling never branches on `name`; pinned vs
  emergent timing respected.
- **Instruction set (guide §4, schema §A10)**: all 8 ops present with the specified
  semantics — RUN demand preserved across preemption, TIMER backlog, FORK cap
  wait-for-slot, unbounded/bounded LOOP, channel WAKE, mailbox.
- **Trace (data-contracts §9)**: exactly the 8 event types (`meta` + `task_arrive`,
  `task_end`, `ready`, `run_start`, `run_end`, `deadline`, `config_applied`);
  diagnostics only under `x_`. Field-level: `ready.cause` covers all five enum
  values; `run_end.reason` ∈ {block,preempt,exit,depart} with `blocked_on` present
  only on `reason=block`; `deadline` carries `due`/`met`/`slack_us`;
  `config_applied` carries `index`/`algorithm`/`provenance`.
- **Config schedule (guide §3)**: first entry at `t_us:0` required (rejected
  otherwise); entries applied in order; same-µs tie-break puts ConfigApply first
  (§9.3 / decision D1); `condition`/`provenance` logged, never branched on; policy
  switch via `handoff()`.
- **Loader (guide §2.1)**: whole-file rejection on any violation (no repair/skip);
  2-pass forward-reference resolution; LOOP flattening.

### Gaps / divergences (against the docs)

1. **`batch_bandwidth_cap` not enforced** — guide §5 ("per-class bandwidth caps,
   enforced by the executor"); the batch-class rule (B1/B2) is fully specified in
   `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md`. The field is not
   even read from the config. This is the experiment's central knob. Out of the A–R
   ladder scope, but a real functional gap.
2. **EDF and lottery policies not implemented** — guide §5 ("needed eventually").
   Only MLFQ and FIFO exist; an EDF/LOTTERY schedule entry is rejected at apply
   time (correctly — no silent fallback). Guide allows building these late.
3. **TIMER `t0` conflict** — code sets `t0` at the *first TIMER execution*
   (`sim.cpp` timer_next init; decision D4), but `metrics.md §11 item 4` states
   `t0` = the task's *arrival time*. guide §9.2 lists this as an open question.
   The two coincide for periodic tasks arriving at `t=0` with a TIMER-first loop
   (all current coreset periodic tasks), so no coreset trace is affected; they
   diverge only for a periodic task arriving mid-run.
4. **No `ready` line for a blocking primitive that completes without blocking** —
   `metrics.md §11 item 1` assumes a `ready` line is emitted at *every* completion
   of a blocking primitive, "at zero wait when it did not block." The code does not:
   a backlog-consumed TIMER tick and a mailbox-satisfied WAIT just advance `pc`.
   Measured: `c1-gaming` emits 4,482 `deadline` but only 218 `ready(cause=timer_tick)`.
   If the harness counts jobs from `ready(timer_tick)` lines (§6.2 B3), this diverges.
5. **`spawn_entry.id` ignored** — schema §A8 marks it required; the code synthesizes
   the child's trace id as `parent.N` instead of using the file's spawn id. The trace
   emits children under the synthesized id.
6. **Loader does not re-check linter invariants** — id uniqueness, `spawn_table`
   present iff FORK, program ends in EXIT or has a `depart`, unbounded LOOP only in
   segment-bound tasks. These are linter invariants the JSON Schema does not enforce;
   the loader trusts the canonical (machine-generated) file.
7. **No output-path / gzip / invocation handling** — data-contracts §11 wants the
   trace gzipped when the output path ends in `.gz`; the code writes JSONL to stdout
   only. `meta.sim` is hardcoded (`"src/sim"`) rather than a version string. The
   invocation contract (`docs/memos/2026-09-11-invocation-contract.md`) was not audited.
8. **§9-open-question decisions not in the normative contract** — D1–D5 (tie-break,
   mailbox, depart, TIMER `t0`, policy switch) are recorded in `../notes/README.md`
   (untracked), but guide §9 wants them absorbed into the contract docs.

### Deferred (cannot be settled from code alone)

- Gaps 3 and 4 are also the behaviour of the reference `sim_r`. Whether the code is
  wrong, or `metrics.md §11` describes the harness's *mock* rather than a hard
  requirement, or the harness in fact reads `deadline` lines — is a contract-reading
  question for 인지오, not decidable from the simulator source.

## 5. Bottom line

The contract skeleton — the 7 non-negotiables, the 8 instructions, the 8 trace
events, the config schedule, determinism, and the whole-file-rejecting loader — is
satisfied and byte-identical to the ladder's final rung across every coreset
workload. The open items are `batch_bandwidth_cap`, EDF/lottery (both beyond the
A–R scope), two genuine doc-vs-code discrepancies (TIMER `t0`, zero-wait `ready`
lines) that are harmless on the current coreset but need 인지오's ruling, and some
invocation-side plumbing (gzip, version string, spawn id).
