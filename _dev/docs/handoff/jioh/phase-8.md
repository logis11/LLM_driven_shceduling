# Handoff — Phase 8 (jioh), written 2026-09-11

Branch `jioh/harness-upper` (off `main` after the Phase 7 merge, PR #5). All Phase 8 work, including `_dev/`, is committed on this branch; `main` has none of it yet. The remote is three commits behind: 8.10's two commits and this handoff are local until pushed.

## Where things stand

- Phase spec: `_dev/docs/spec/jioh/phase-8-harness-upper-half-through-pre-registration.md` (21 decisions, three dated amendments).
- Done: **8.1** boot default from OSTEP (`task-8.1-boot-default-from-ostep.md`, memo `docs/memos/2026-09-11-boot-default-from-ostep.md`), **8.2** scorer (`task-8.2-scorer.md`, 9 decisions), **8.10** boost windows (decided inside 8.2's spec, decision 9).
- Harness state: `make -C harness lint` clean, 94 tests green under `/usr/local/bin/python3.12` (the only local interpreter with the pinned deps; `python3` on this machine lacks them). Records have 21 columns (`boot_default` added). New modules `aggregates.py`, `scorer.py`, `outputs.py`, CLI `tools/score.py`, schemas under `harness/aggregates/schema/` and `harness/scores/schema/`, fixture `tools/tests/fixtures/mock-scores/`.

## Next: 8.3 guard spec and guards

Startable (8.3 ∥ 8.4 ∥ 8.5). What 8.3 must deliver, from the phase spec (decisions 6, 7): a guard spec data file beside the scoring spec (the eight guards: provenance share, config age, starvation floor, determinism, utilisation sanity, tick count, `validation` equals `provenance`, the C2 pair check; thresholds with grounding; schema; lint), guard code, the hand-written `held`/`clamped` schedule fixture, tests. Guards read the `aggregates` file (8.2) where an aggregate exists (fallback share, config-age distribution, starvation max, utilisation, counts) and traces or records where not (determinism hashes, C2 identical-trace check). The evaluator (8.7) will emit `invalid` on a failed non-exempt guard; exemptions are per-experiment data, not guard code. Thresholds are numbers: each needs a grounding argued in 8.3's grill.

## Open threads

- **인경민's two executor rules** (memo §5): whether a waking deadline task preempts a residual slice, and same-instant order of slice boundary vs TIMER expiry. Their answer decides `c7-meeting`/`c7-media` (expected no headroom on the arithmetic, knife edge) and those files' judging-set membership, re-decided in 8.8. Memo not yet sent to the team as far as this session knows.
- **Boot-default sensitivity pair**: the team's to pick (candidates illumos 2 ms, Linux 0.75 ms, sched_ext 20 ms); written into the RQ0 gate spec in 8.8. The records column and the scorer already handle any list.
- **Scoring spec and guard spec freeze**: 인지오 alone in 8.8, harness changelog; team ratification at a meeting afterwards (user's call).
- **Docs sweep (8.9)**: the Korean harness guide still says twenty columns and describes the scorer as future; terminology entries for RQ0 gate evaluator, per-experiment spec, guard spec, driver table tuning set; the "throwaway pool" rename across nine files.
- **No archive written** for Phase 8 yet (archives only on request).
