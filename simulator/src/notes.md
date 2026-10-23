# src/sim.cpp — build notes and conformance audit

> Working notes for the reference simulator in this directory. Records what `sim.cpp`
> currently implements, how it was verified, and where it stands against the repo's
> contract documents. Not a normative spec — the contracts under `docs/` win.

## 1. What this is

`sim.cpp` is a one-lane discrete-event scheduler simulator: a pure function
`(workload.json, config-schedule.json?) → JSONL trace`. It was carried from an
earlier snapshot (stage I: core + MLFQ + preemption + gen, with a hardcoded `main`
and no loader) to **stage R** (full instruction set, workload loader, config
schedule with policy handoff) and then **stage S** (EDF + LOTTERY — all four algorithms of
the frozen menu), **stage T** (children traced under their spawn_table id) and **stage U**
(config-switch semantics: MLFQ cold start, same-algorithm entries, drain), matching the
one-rung-at-a-time ladder in `../steps/`.

**2026-10-23 (X — conformance (a), with Q2):** a `ready` line at every completion of a blocking
primitive, at zero wait when it did not block — a WAIT met from a mailbox, a TIMER in backlog, tick 0
in the arrival step — and RUNs joined without a block are one occupancy: `boundary()` steps the
holder on its lane with no requeue and no pick, writing `x_run_cont`. A lone holder's slice expiry
writes no `run_end`/`run_start` pair (Q2). Closes §4 items 4 and 10. Ladder rung `steps/sim_x.cpp`;
`src/sim == steps/sim_x` 128/128. Verified against the contract rather than the previous binary
(every MLFQ trace changes): the harness hand fixtures line by line, conservation laws, and the
harness's own guards — lane violations 717,297 → 0 and guard messages 187,733 → 73,271 over 128
local runs, the rest being (b)'s and unconsumed input at the run's end. Fixed beside it: a task
that EXITs before its depart no longer writes a second `task_end`. Detail: `../steps/README.md`,
the x rows.

**2026-10-21 (W — spawn-table `WAKE` targets):** the loader resolves a `WAKE` target that names a
spawn-table entry, not only a top-level `arrive` id, and holds a wake that lands before the child's
birth. Without it the rebuilt build's compile files do not load at all (§4 item 13). The ladder rung
`steps/sim_w.cpp` followed on 2026-10-23 (인지오's answer, memo_261021 H3), so
`src/sim == steps/sim_<last>` holds again: 128/128 with `meta.sim` normalised. Negative control
120/120 byte-identical to the pre-W binary on the local build; positive control on two fixtures
built by the dataset's own `_object_job`/`_tree_job`. Status: `../memo/memo_261021.md` Part E.

**Ported 2026-10-20 (V — `batch_bandwidth_cap`):** the executor now applies the cap as a
work-conserving ceiling on the behavioural batch class (RQ0 conformance item (d)). The accounting
window is a token bucket, rate = cap and depth = one slice (decision D10, `../steps/README.md`).
`src/sim` equals `steps/sim_v` byte for byte on 96 coreset runs (24 files × 4 schedules) and 18
hand-workload runs, `meta.sim` normalised. Verification and the two defects found on the way:
`../steps/README.md`, the v rows; status `../memo/memo_261020.md` Part F.

**Ported 2026-10-10 (T + U):** `src/sim` equals `steps/sim_u` byte for byte after normalizing
`meta.sim`. The check covered 25 workloads (the 24 coreset files plus the harness
`mock-switch` run file) under 4 schedules each: none, the one-entry boot default, the
`mock-switch` schedule, and a 9-entry four-algorithm stress schedule. Result 100/100. The
pre-port binary differs on `c1-compile`, which serves as the positive control. Details:
`../memo/memo_261010.md` Part B.

Build:
```
g++ -std=c++17 -O2 -Wall -Wextra -o sim sim.cpp
./sim <workload.json> [<config-schedule.json>]      # trace → stdout (JSONL)
```
`sim.cpp` depends on `mini_json.hpp` (in this directory).

## 2. Stages implemented (A–X)

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
| S | EDF + LOTTERY behind a third seam, `TaskView` (executor-owned classes: B2 periodic, B1 batch); WAKE carries the waker's deadline down a chain; lottery PRNG seeded from the workload id; `Policy::start(params, cold)`; policy-timer epoch (fixes an R hang, §4 item 9) |
| T | a spawned child is traced under its `spawn_table` id, not a synthetic one (fixes §4 item 5) |
| U | config-switch semantics: U1 a switch into MLFQ is a cold start, U2 a same-algorithm entry leaves the holder and the queue order alone, U3 a switch out of MLFQ/EDF/LOTTERY drains until the lane is free |
| V | `batch_bandwidth_cap` enforced — conformance (d). Token bucket (D10: rate = cap, depth = one slice), `park`, the cap's own timer, one-way state transitions through `set_st` (fixes §4 item 1) |
| W | the loader resolves a `WAKE` target that names a **spawn-table entry**, not only a top-level `arrive` id — conformance item (i), see §4 item 13 (2026-10-21) |
| X | a `ready` line per completed blocking primitive, zero-wait ones included; RUN→RUN in one occupancy (`boundary()`, `x_run_cont`); a lone slice expiry keeps the lane with no `run_end` (Q2); a RUN ending at the µs of another decision is settled by its own Lane event — conformance (a) (2026-10-23; fixes §4 items 4 and 10) |

## 3. Verification performed

**Stage S (2026-10-01)** — against `../steps/sim_s.cpp`, normalizing only `meta.sim`:

- **Regression**: with no schedule and with an MLFQ→FIFO schedule (no MLFQ re-entry), `sim_s`
  is byte-identical to `sim_r` on all 24 coreset files (48/48).
- **New paths**: mock-switch, EDF-only, LOTTERY-only (`batch_share` 0.15), and an 8-entry
  MLFQ→EDF→LOTTERY→FIFO→LOTTERY→LOTTERY→EDF→MLFQ schedule — all 24 files terminate, rerun
  byte-identical, and `src/sim` == `sim_s` (96/96).
- **Behaviour** (hand workloads): `edfheavy` (TIMER 16.7 ms, 12 ms burst, plus a hog) — EDF
  meets 599/599, MLFQ 0/250. `share2` (one periodic task + one hog, both always runnable) —
  the batch class gets 14.8% at `batch_share` 0.15 and 49.1% at 0.5. Seed control: changing
  only `meta.id` changes a LOTTERY trace.

The stage-R record below stands for R's own scope:

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

1. ~~**`batch_bandwidth_cap` not enforced**~~ — **done in stage V (2026-10-20).** The loader
   reads the field (null → no ceiling) and the executor applies it to the batch class while a
   non-batch task is runnable. The accounting window the batch memo §7 item 3 left to this tree
   is D10: a token bucket, rate = cap, depth = one slice, so contiguous batch interference is
   bounded by the quantity the algorithm already imposes on everyone and no new constant is
   invented; the implied window is slice/cap. Remaining in this area: the two unit tests of the
   batch memo §7.6, the `x_batch_class` diagnostic (V emits `x_cap_park` instead, which records
   the throttle rather than the class), and checking that the rebuilt core set's batch tasks
   enter the class as §4 predicts. Two consequences need 인지오's confirmation, both in
   `../memo/memo_261020.md` Part F: under FIFO the cap must preempt, since a ceiling over a
   non-preemptive algorithm has no other lever; and a stretch that opens mid-occupancy leaves a
   debt rather than re-arming the holder, bounded by one grant (measured: one bucket depth).
2. ~~EDF and lottery policies not implemented~~ — **done in stage S.** Remaining:
   no executor starvation safety net (EDF's deadline class and FIFO have no horizon); no
   range clamping or cross-field rule 5 (`batch_share ≤ cap`) in the loader — like MLFQ, it
   trusts the composed config upstream. Under FIFO the B1 threshold uses the boot default's
   `timeslice_us` (10000) — the boot-default memo §5 already says to read the batch-class
   memo's "2000 µs" as 10000.
3. **TIMER `t0` conflict** — code sets `t0` at the *first TIMER execution*
   (`sim.cpp` timer_next init; decision D4), but `metrics.md §11 item 4` states
   `t0` = the task's *arrival time*. guide §9.2 lists this as an open question.
   The two coincide for any periodic task whose program starts with its TIMER, so no
   coreset trace is affected. *(Corrected 2026-10-01: 12 periodic tasks do arrive
   mid-run — `c3-evening`, `c4-compile` — but all are TIMER-first; the earlier "all
   arrive at t=0" was wrong.)* Guide §9.2 leaves the pick to the builder, so this is
   ours to pin, not a question for 인지오.
4. ~~**No `ready` line for a blocking primitive that completes without blocking**~~ — **fixed in X
   (2026-10-23)**, with item 10. The record as it stood —
   `metrics.md §11 item 1` assumes a `ready` line is emitted at *every* completion
   of a blocking primitive, "at zero wait when it did not block." The code does not:
   a backlog-consumed TIMER tick and a mailbox-satisfied WAIT just advance `pc`.
   Measured: `c1-gaming` emits 4,482 `deadline` but only 218 `ready(cause=timer_tick)`.
   If the harness counts jobs from `ready(timer_tick)` lines (§6.2 B3), this diverges.
5. ~~**`spawn_entry.id` ignored**~~ — **fixed in T (2026-10-10).** The loader dropped the
   spawn entry's `id`, and children were traced as `parent.N` (`build.1`). The harness
   `reader.py` registers them as `build.c1`. Children are now traced under the file's id.
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

9. **Fixed in S — policy timers outlived a config apply.** Each MLFQ `start()` armed one more
   boost chain and none was cancelled; the chains kept each other alive past `arm()`'s stop
   rule. `sim_r` on `c1-compile` × mock-switch never terminates (measured: 24M lines,
   virtual t ≈ 45 h after 15 s). Fixed with a config epoch on `PolicyTimer`. Changes traces only
   for schedules that re-enter MLFQ.
10. ~~**Not fixed — a RUN→RUN boundary without a block breaks the occupancy record.**~~ **Fixed in X
   (2026-10-23)**: one occupancy, `x_run_cont` at each boundary, the zero-wait line inside it; the
   lone-holder slice expiry of Q2 goes with it. The record as it stood — When a
   RUN ends and the next instructions reach another RUN without blocking (WAKE, backlogged
   TIMER, mailbox-satisfied WAIT, FORK), `advance()` emits `ready cause=arrive`, gives up
   the lane **without a `run_end`**, and requeues the task. Boot MLFQ: 35,803 of 86,239
   `ready` lines in `c1-gaming` (41%), 43,098 of 175,443 in `c2-p2b`. metrics.md §6 expects a
   zero-wait `ready` with the real cause *inside* the task's own occupancy, and guide §5 says
   there is nothing to decide between events — so the holder should keep the lane. The
   trace-clarifications memo (2026-09-07) §4 already answers it: emit the line "with the task
   already running", no fake `run_end`/`run_start`. Not a question — owed implementation,
   and the top priority: the harness's `records.py` on unchanged `sim_r` traces raises 4,798
   guards on `c1-media` alone (no `ready(timer_tick)` for tick 0, so every job is paired one
   iteration late and reads as a miss). The fix also closes item 4 and changes every MLFQ
   baseline trace. Under LOTTERY it also means a re-draw at every RUN boundary.
11. **EDF collapses on the gaming files — because of how chain stages are classed.**
   `c1-gaming` under EDF meets 5 of 5,664 deadlines. *(Corrected 2026-10-01: this was first
   written up as "overload, not a bug". The overload is real — utilization 1.46 per the
   coreset guide — but the head's and the compositor's deadlines collapse only because S puts
   the 16 WAKE-driven chain stages in the deadline class; with that off, 7,372/7,372 are met.)*
   The docs disagree on that class (vocab §2 and the pair review vs batch-class memo B2), and
   it flips `c2-p2b`'s frames under EDF from 0% to 99.8% missed — asked of 인지오 in
   `../notes/note-for-jioh-edf-chain-stage-class.md`. **Answered 2026-10-10: deadline class,
   inherited deadline (head tick + one period) as implemented — no code change.** The EDF numbers
   must be re-measured once 인지오's dataset rework lands (`c1-gaming` loses the compositor;
   `c2-p2b`'s clamscan becomes unattended-upgrade).
12. **Fixed in S — EDF slice-boundary preemption.** A residual task preempted in the same µs
   as its slice end kept the fully used slice, so its next dispatch had horizon 0 (600
   zero-length occupancies on the boot-default memo's video/music/scan scenario). Now counted
   as a slice end. The status of everything above is recorded in `../memo/memo_261001.md`.
13. **Fixed in W — a `WAKE` naming a spawn-table entry rejected the whole file.** `compile_prog`
   resolved every target against the top-level `arrive` id table, so the rebuilt build's make
   jobs — six member processes waking each other by spawn-table id (9.6 D19), and the module
   build's trees of 6/6/8/10 (9.10 D53) — failed to load: `"WAKE target is not a top-level
   task: build.j1.gcc"`. It rejected `c1-compile`, `c7-compile` (both judging files),
   `c3-workday`, `c4-compile`, `c6-dual`, 8 compile variants and 188 generated files. Found by
   the 2026-10-10 dataset audit as blocker 1; relayed in the 2026-10-17 rebuild memo. It is
   **not** one of the eight `simulator-conformance` items. W resolves such a target to a
   negative slot that the child's birth fills, and **holds** a wake that arrives before the
   birth instead of dropping it — `fork_cap` is a multiple of six while the trees are 8 and 10
   members, so the cap splits a job and a job's root can wake a member not yet forked; dropping
   it deadlocks the job (measured: 6 of 13 and 10 of 19 tasks never end). Details and the
   negative/positive controls: `../memo/memo_261021.md` Part E.
   **Invisible on the local build** — the 2026-09-04 build predates the structure and its
   `c1-compile` has zero child WAKE targets, so this and the rebuild have to land together.

### Deferred (cannot be settled from code alone)

> **Indexed in `../memo/memo_261021.md` Part B**, the single entry point for everything addressed to 인지오.

- ~~Gaps 3 and 4 are also the behaviour of the reference `sim_r`. Whether the code is
  wrong, or `metrics.md §11` describes the harness's *mock* rather than a hard
  requirement, or the harness in fact reads `deadline` lines — is a contract-reading
  question for 인지오, not decidable from the simulator source.~~

  **Both settled; nothing deferred here (corrected 2026-10-21).** This paragraph predates the
  RQ0 gate spec's `simulator-conformance` statement, which answers it:

  - **Gap 4 is conformance item (a)**, ratified as a requirement — "a ready line at every
    completion of a blocking primitive, at zero wait when it did not block, inside the occupancy
    after the run_start (metrics doc §11 item 1)". So `metrics.md` §11 item 1 is a hard
    requirement, not a description of the mock, and the code is the side that is wrong. Owed.
  - **Gap 3 is ours**, as gap 3's own last sentence says: guide §9.2 leaves the pick to the
    builder. It is on `_dev/TODO.md` under "Ours to decide" as TIMER t₀, D4.

## 5. Bottom line

The contract skeleton — the 7 non-negotiables, the 8 instructions, the 8 trace
events, the config schedule, determinism, and the whole-file-rejecting loader — is
satisfied and byte-identical to the ladder's final rung across every coreset
workload — through X (`steps/sim_x`, 2026-10-23).

`batch_bandwidth_cap` (V) and EDF/lottery (S) are done. What is open, as of 2026-10-23, is the
`simulator-conformance` statement of `harness/experiments/rq0-gate.yaml`: **(a), (c), (d), (f), (i)
met; (b) the TIMER skip rule, (e) the strict idle class, (g) `WAIT children:<id>`, (h) the
invocation contract still owed.** (a) is met on the local build; the gate spec's own sentence
still reads "(c), (d), (f) and (i)" — its edit is 인지오's, with a harness changelog entry. The RQ0 run does not start until
all eight are shown. Beside them: TIMER `t0` (§4 item 3) still needs 인지오's ruling, and the
remaining invocation plumbing is (h). The regression baselines all stand on the stale 2026-09-04
24-file build while the dataset is rebuilt to 51 files plus 78 variants — re-baselining is the
precondition for (e) and for checking W on real files, and it is 인지오's to run.
