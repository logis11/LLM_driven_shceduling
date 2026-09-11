# Handoff — Phase 8 (jioh), written 2026-09-11

Branch `jioh/harness-upper`, off `main` after the Phase 7 merge (PR #5). All Phase 8 work, `_dev/` included, is committed there; `main` has none of it. The remote is current through the 8.3 session; the 8.4 commits are local until pushed.

## Where things stand

- Phase spec: `_dev/docs/spec/jioh/phase-8-harness-upper-half-through-pre-registration.md` (21 decisions, three dated amendments).
- Done: **8.1** boot default, **8.2** scorer, **8.10** boost windows, **8.3** guard spec and guards, **8.4** L1 grader.
- **175 tests green**, three lints clean (fixtures, scoring spec, guard spec) under `/usr/local/bin/python3.12` — the only local interpreter with the pinned deps, so every command needs `PY=/usr/local/bin/python3.12`. Dataset `make check` and the daemon's driver-table lint both pass. The harness lint needs the compiled coreset: `make -C dataset dataset` first.

## Next: 8.5 — invocation contract and mocks

The only startable sub-task. Three deliverables, from phase spec decisions 9, 10, and 11.

**The invocation contract (decision 9).** The runner fixes one command shape for both the daemon and the simulator: input paths and the condition in, output paths out, an exit code, and no other channel. The mock daemon and mock simulator are its first two implementations, and 인경민 and 박이안 meet it when they deliver. It goes into `docs/data-contracts.md` with a changelog entry and is told to both. Note that this is a **new** contract rather than a change to a frozen one, so §12's all-three-signatures rule does not gate writing it; whether it freezes is 8.5's own call. The doc's contracts currently run 1 to 9 across §2 to §10, so this becomes a new section.

**The mock daemon (decision 11).** Faithful for `fixed`, `oracle`, and `random` only. It walks the visible projection's pinned events for query points, reads ground truth or draws, maps through the **prior** table, and emits contract-valid config schedules (§7) and recognition logs (§8) for any coreset file. It emits `unmodified` only — no validator, no clamping, no `held`, no LLM path — and lives in the harness test tree, discarded in Phase 9. `mock-guards` already supplies the hand-written schedule that covers `held` and `clamped` for the guards, precisely because the mock daemon will not produce them.

Two rules it must implement exactly, both already written down. Query points are the five telemetry rules in data-contracts §5: the set is a name-to-count multiset so a count-only change counts; all pinned events at one timestamp produce exactly one snapshot; `processes` is sorted by name so reruns are byte-identical; the snapshot at the workload's final instant is emitted and logged like any other; nothing else emits one. And `random`'s draw is phase spec decision 15: at every set change, one uniform draw over the 32 driver-table rows, independent of previous draws and of the telemetry, from a seeded generator, logged with its draw and seed, at zero latency.

One known edge: inside `c6-dual`'s `ambiguous` segment the oracle's answer is undefined per the daemon guide, and under the rules as written it is rejected and the file runs on fallback. The grader already excludes those query points, so nothing downstream breaks, but the mock must not pretend otherwise.

**The mock simulator (decision 10).** Both a trivial generator and a replay. The generator emits a contract-valid trace (§9) for any coreset file and schedule from a trivial rule with **no scheduling modelled at all** — it never models a queue — so all 50 files flow through the whole pipeline. The replay returns the hand-written fixture traces so values stay checkable. Both live under `harness/`, never under the simulator tree, and are discarded in Phase 9.

**What already consumes their output, unchanged.** The readers for trace, run file, config schedule, and recognition log are all in `harness/tools/harness/reader.py`. A config schedule feeds the records builder and the guards; a recognition log feeds the grader (`tools/grade.py`) and the `validation` equals `provenance` guard; a trace feeds records. So if the mocks are contract-valid, nothing above them needs touching.

**One thing 8.5 retires.** In 8.4 the graded-set profile was derived once by hand-applying the telemetry rules to the compiled coreset, because no log existed. The mock daemon is the real implementation of those rules, so from 8.6 onward the counts come out of the grades file and the one-off derivation can be forgotten.

Then: **8.6** runner with execution cache, which writes the guards and grades manifests and owns the determinism rerun policy; **8.7** per-experiment spec schema, RQ0 gate evaluator, report — it also inherits the `random-beats-oracle` flag from 8.3 as a non-blocking per-judging-file report line, not a guard; **8.8** pre-registration and the freeze; **8.9** docs sweep.

## Conventions worth not relearning

- Segments are half-open, `t_start <= t < t_end`, everywhere. The terminal snapshot at exactly `t_end` is therefore uncovered by design.
- A records file is per source artifact. Recognition rows leave `sim` empty and the schema no longer requires it.
- The harness never imports the daemon's or the dataset's modules. Where it must reproduce their logic, a test pins the two together — `compose_row` against the daemon's `compose` on every row of the prior table is the precedent.

## Measured facts worth not rediscovering

Derived from the compiled coreset on 2026-09-11 and recorded in the 8.4 spec: 134 query points, 50 terminal and 2 `ambiguous` skipped, **82 graded over 49 files**, 10 carrying `pre_committed_miss`, so the headline set is **72 over 44**. The attribute majority baseline is 69.5 per cent and mode's is 11.0, which is why the attribute is corrected and mode is not. Files contribute 1.67 graded points on average, 22 of them exactly one.

## Open threads

- **인경민's three questions** (8.1 memo §5): the two executor rules, which decide `c7-meeting`/`c7-media` and their judging-set membership in 8.8, and the executor's starvation window, which replaces the `starvation_floor` guard's 1 000 000 µs stated assumption. Memo not yet sent as far as this session knows.
- **Boot-default sensitivity pair**: the team's to pick; written into the RQ0 gate spec in 8.8.
- **Freeze (8.8)**: scoring spec and guard spec (bump the guard spec from 0.1) by 인지오 alone, in a harness changelog that does not exist yet; team ratification afterwards.
- **Docs sweep (8.9)**: the harness guide's missing chapters for the upper half, terminology entries (RQ0 gate evaluator, per-experiment spec, guard spec, driver table tuning set), docs index, the "throwaway pool" rename across nine files.
- **Layer 1 is underpowered** for the whitelist comparison at 44 to 49 independent units, and the familiarity contrast at tiers 4 and 5 rests on one graded query point per tier. Both are stated in the 8.4 spec rather than left to be discovered.
- **The familiarity experiment** needs its own per-experiment spec; run-to-run consistency stays blocked on the recognition log's missing repeat index.
- **No archive written** for Phase 8 (archives only on request).
