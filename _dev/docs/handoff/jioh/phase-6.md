# Handoff — Phase 6: 6.1 done, 6.2 picked up

Written 2026-09-09. Repo `LLM_driven_shceduling`, branch `jioh/driver-table-v0` (off `main` after PR #4; `_dev/` edits land on this branch by the user's call). Pushed at handoff time.

## Where things stand

- **Phase 6 `[WIP]`**, spec `_dev/docs/spec/jioh/phase-6-driver-table-v0-and-scoring-spec.md`. Order 6.1 → 6.2 → 6.3 → 6.4.
- **6.1 Switch overhead — done.** `switch_window` primitive (lane-time window: closes when the last hog has received `W_single` of CPU since `t_apply`; clipped at the next switch or `T_end` with a guard), `hogs` twentieth records column, config schedule as the harness's third input (`--schedule`, matched by `index`, cross-checked against the trace), `x_mlfq_level` check tool `harness/tools/check_mlfq_levels.py`, fixture `mock-switch`. 63 tests, lint clean. Metrics doc §3/§5/§6.9/§8/§11/§12/§13; memo §7 revision.
- **Settled with 인경민 on 2026-09-09** (memo §5/§7, metrics doc §11 items 7–9): a same-algorithm entry applies at its stamped time with queue levels kept and is not a switch; FIFO-outgoing applies immediately with the running task freshly dispatched (rule a); the boost timer restarts at `t_apply`. Nothing on the switch semantics is open.
- **Mocks follow the guide's MLFQ rules and the memo** (fixtures README item 7). `mock-p1a` was rewritten to them; `mock-chain` and `mock-media` run FIFO under an oracle entry beside the boot entry.
- **6.2 Scoring spec — `[WIP]`, not started.** Next: brief from the spec's decisions 5–15, then implementation test-first (the user's route; no plan doc, no worktree).

## 6.2 inputs

- Spec decisions 5–15: term shape, scored aggregates (P99 / miss rate / progress / makespan), per-file weights, C2 window 60 s–`T_end`, derived files equal their base, `c6-dual` two foregrounds, `c1-idle` none, placement (YAML in the harness tree, JSON schema, lint, CI) and the lint's checks.
- Entity names from `dataset/build/coreset-single/*.workload.json` (task ids: `editor`, `hog`, `writer`, `browser`, `game.chain.1`, `video`, `music`, `build`, `bulk`, `download`, `batch`, `photo-editor`, `video-editor`, `mailer`, `compositor`, `spoof`, …) — read them, do not guess; the lint enforces existence.
- Metrics doc §8 for the aggregate vocabulary; §9 floors are not the scoring spec's.
- Harness tree conventions: `harness/README.md`, `harness/Makefile`, `.github/workflows/harness.yml`, `harness/records/schema/` (machine schemas beside the code).

## Rules of this project the session must keep

- Archives only on explicit request (`CLAUDE.md`). Do not propose or announce one.
- One question per message in grills; plain chat, no AskUserQuestion.
- Nothing enters code or docs that is not a field or rule in the contracts, the metrics doc, or the spec.

## Environment

- venv in the session scratchpad: `pip install -r dataset/tools/requirements.txt -r daemon/tools/requirements.txt -r harness/tools/requirements.txt`; pass `PY=<venv>/bin/python` to the Makefiles.

## Carried forward (not 6.2's)

- 박이안 on the repeat index; `c1-media` tier-1 familiarity annotation; C1-derived `demand: calibration`; gate spec items (Phase 7).
