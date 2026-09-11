# Handoff — Phase 8 (jioh), written 2026-09-11

Branch `jioh/harness-upper` (off `main` after the Phase 7 merge, PR #5). All Phase 8 work, including `_dev/`, is committed on this branch; `main` has none of it yet. Local commits since the last push: 8.10's two, the previous handoff, the 8.3 WIP mark, the 8.3 spec, the 8.3 implementation, and this handoff.

## Where things stand

- Phase spec: `_dev/docs/spec/jioh/phase-8-harness-upper-half-through-pre-registration.md` (21 decisions, three dated amendments).
- Done: **8.1** boot default from OSTEP (`task-8.1-boot-default-from-ostep.md`), **8.2** scorer (`task-8.2-scorer.md`), **8.10** boost windows, **8.3** guard spec and guards (`task-8.3-guard-spec-and-guards.md`, 17 decisions).
- Harness state: `make -C harness lint` clean (three lints: fixtures, scoring spec, guard spec), 122 tests green under `/usr/local/bin/python3.12` (the only local interpreter with the pinned deps). New in 8.3: `harness/guards/` (guard spec 0.1, two schemas), `tools/harness/guards.py` (registry, `evaluate`, lint), `read_recognition_log` in the reader, CLIs `tools/guards.py` (run manifest + aggregates → guards CSV, exit 2 on a fail) and `tools/guards_lint.py`, fixture `mock-guards`.

## Next: 8.4 ∥ 8.5

Both startable. **8.4** L1 grader: reuse `read_recognition_log`; `pre_committed_miss` from ground truth; balanced accuracy with the confusion matrix per familiarity tier; the with-and-without-exclusion line. **8.5** invocation contract and mocks: the command shape into the data-contracts doc with a changelog entry; mock daemon and mock simulator under `harness/`. Then 8.6 (runner: writes the guards manifest, owns the determinism rerun policy), 8.7 (evaluator: `invalid` on a failed non-exempt guard; the `random-beats-oracle` report flag handed over from 8.3), 8.8, 8.9.

## Open threads

- **인경민's two executor rules** (8.1 memo §5): decide `c7-meeting`/`c7-media` and their judging-set membership, re-decided in 8.8. Memo not yet sent as far as this session knows.
- **인경민's starvation window**: the starvation guard's 1 000 000 µs bound is a stated assumption until the executor's declared window replaces it (guard spec grounding; changelog entry when it lands).
- **Boot-default sensitivity pair**: the team's to pick; written into the RQ0 gate spec in 8.8.
- **Freeze (8.8)**: scoring spec and guard spec (bump guard spec from 0.1) by 인지오 alone, harness changelog (does not exist yet); team ratification afterwards.
- **Docs sweep (8.9)**: the harness guide still says twenty columns and describes the scorer as future; terminology entries for RQ0 gate evaluator, per-experiment spec, guard spec, driver table tuning set; the "throwaway pool" rename across nine files.
- **No archive written** for Phase 8 yet (archives only on request).
