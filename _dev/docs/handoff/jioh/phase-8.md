# Handoff — Phase 8 (jioh), written 2026-09-11

Branch `jioh/harness-upper`, off `main` after the Phase 7 merge (PR #5). All Phase 8 work, `_dev/` included, is committed there; `main` has none of it. The remote is current through the 8.3 session; the 8.4 commits are local until pushed.

## Where things stand

- Phase spec: `_dev/docs/spec/jioh/phase-8-harness-upper-half-through-pre-registration.md` (21 decisions, three dated amendments).
- Done: **8.1** boot default, **8.2** scorer, **8.10** boost windows, **8.3** guard spec and guards, **8.4** L1 grader (`task-8.4-l1-grader.md`, 21 decisions).
- Harness state: three lints clean (fixtures, scoring spec, guard spec), **175 tests green** under `/usr/local/bin/python3.12`, the only local interpreter with the pinned deps. Dataset `make check` and the daemon's driver-table lint both still pass.
- New in 8.4: records have **22 columns** (`pre_committed_miss`) and `sim` is no longer required; a fifth recognition primitive `config_correct`; `harness/grades/` with the grades schema; `tools/harness/grader.py`; CLI `tools/grade.py` on a run manifest; fixture `mock-grades`; four verified references (`brodersen-icpr10`, `chicco-bmcg20`, `field-jrssb07`, `dietterich-neco98`).

## Next: 8.5, then 8.6

**8.5** invocation contract and mocks is the only remaining startable sub-task: the command shape into the data-contracts doc with a changelog entry, plus the mock daemon (faithful for `fixed`/`oracle`/`random`, no validator) and the mock simulator (a trivial generator plus replay of the hand fixtures), both under `harness/` and discarded in Phase 9. Then 8.6 (runner, which writes the guards and grades manifests and owns the determinism rerun policy), 8.7 (per-experiment spec schema, RQ0 gate evaluator, report), 8.8 (pre-registration and the freeze), 8.9 (docs sweep).

Two things 8.4 hands forward. The `random-beats-oracle` flag goes to 8.7 as a non-blocking per-judging-file report line, not a guard. And once 8.5's mock daemon produces logs for all fifty files, the graded-set profile stops being a one-off derivation and becomes an output of the grades file.

## Measured facts worth not rediscovering

Derived from the compiled coreset on 2026-09-11 and recorded in the 8.4 spec: 134 query points, 50 terminal and 2 `ambiguous` skipped, **82 graded over 49 files**, 10 carrying `pre_committed_miss`, so the headline set is **72 over 44**. The attribute majority baseline is 69.5 per cent and mode's is 11.0, which is why the attribute is corrected and mode is not. Files contribute 1.67 graded points on average, 22 of them exactly one.

## Open threads

- **인경민's three questions** (8.1 memo §5): the two executor rules, which decide `c7-meeting`/`c7-media` and their judging-set membership in 8.8, and the executor's starvation window, which replaces the `starvation_floor` guard's 1 000 000 µs stated assumption. Memo not yet sent as far as this session knows.
- **Boot-default sensitivity pair**: the team's to pick; written into the RQ0 gate spec in 8.8.
- **Freeze (8.8)**: scoring spec and guard spec (bump the guard spec from 0.1) by 인지오 alone, in a harness changelog that does not exist yet; team ratification afterwards.
- **Docs sweep (8.9)**: the harness guide's missing chapters for the upper half, terminology entries (RQ0 gate evaluator, per-experiment spec, guard spec, driver table tuning set), docs index, the "throwaway pool" rename across nine files.
- **Layer 1 is underpowered for the whitelist comparison** at 44 to 49 independent units, and the familiarity contrast at tiers 4 and 5 rests on one graded query point per tier. Both are stated in the 8.4 spec rather than left to be discovered.
- **The familiarity experiment** needs its own per-experiment spec; run-to-run consistency stays blocked on the recognition log's missing repeat index.
- **No archive written** for Phase 8 (archives only on request).
