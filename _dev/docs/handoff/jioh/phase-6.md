# Handoff — Phase 6 spec'd, 6.1 not started

Written 2026-09-08 at the end of the Phase 6 spec session. Repo `LLM_driven_shceduling`, branch `jioh/driver-table-v0` (fresh off `main` after PR #4 merged Phase 5; `_dev/` edits land on this branch by the user's call). Pushed at handoff time.

## Where things stand

- **Phase 6 is `[WIP]` and spec'd.** Spec: `_dev/docs/spec/jioh/phase-6-driver-table-v0-and-scoring-spec.md`. Sub-tasks 6.1–6.4 inlined in `_dev/TODO.md`, strict order 6.1 → 6.2 → 6.3 → 6.4. None started, none `[WIP]`.
- **Next action**: `daily-work-harness:pick-up-task` → pick **6.1 Switch overhead**, mark `[WIP]`, brief, then straight to implementation with TDD (the user's route for code: failing test first, no plan doc, no worktree).
- **No archive yet.** The user archives once per phase, at phase end. The spec session's decisions and verified facts are in the spec and in the session transcript; the archive at phase end must carry the grill's rationale (Q1–Q17) and the facts below.

## 6.1 inputs (do not re-derive)

- The memo defining the work: `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` §4 (window `W_single · H`, hog count rule, excess aggregate, boost baseline, `x_mlfq_level`) and §6 harness side (five items).
- Metrics doc `docs/harness/metrics.md`: §5 records (nineteen columns today; 6.1 adds `hogs`), §6 primitives, §8 aggregates, §11 assumptions (add the boost-timer restart at `t_apply` as a stated assumption), §13 changelog.
- Harness code: `harness/tools/harness/{reader,primitives,records}.py`, schema `harness/records/schema/records.schema.json`, fixtures `harness/tools/tests/fixtures/*/{run.json,trace.jsonl,expected.csv,worked.md}`, `make -C harness lint|test` (43 tests green at handoff).
- The check tool reads `x_mlfq_level` lines, which the harness reader ignores by the `x_` rule; it lives beside the harness, not inside it.

## Facts verified in the spec session (for the archive)

- Coreset `ground_truth` exercises 18 `(mode, background_wanted)` keys; 17 legal (minus `ambiguous`), 16 in C1–C4 (`meeting/true` is c6-fold only). Only two `wanted=false` rows: `gaming/false` (c2-p2b), `indexing/false` (c2-p1b). The notes' "likely under ten" was wrong.
- Of the three C2 pairs only p2 is a same-mode pair; p1 is `ml-train/true` vs `indexing/false`, p3 is `render/true` vs `backup/true`.
- `c1-media` cannot miss a tick under any legal configuration (video needs > 10 ms wait, music can cause 2.5 ms; music needs > 47.5 ms, video can cause 6.67 ms) → "no headroom" expected; same for `c3-evening`'s media segment and C5.
- `c3-creation`'s HandBrake runs uncontended after 240 s (kdenlive unfocused) → progress term "no headroom" expected.
- The simulator tree is a single 128-line `sim.cpp` with no policy code; the table's algorithms are a requirement on 인경민 before Phase 8.
- The lint does not enforce `basis: theory` on the prior table; the contract sentence does.

## Environment

- venv in the session scratchpad: `pip install -r dataset/tools/requirements.txt -r daemon/tools/requirements.txt -r harness/tools/requirements.txt`; pass `PY=<venv>/bin/python` to the Makefiles. Recreate each session.

## Open items carried forward

- Memo replies: 인경민 on trace clarifications, switch semantics (FIFO-outgoing rule, boost timer at `t_apply`); 박이안 on the repeat index.
- `c1-media` tier-1 familiarity annotation; the word "familiarity"; C1-derived `demand: calibration`; gate spec items (Phase 7).
