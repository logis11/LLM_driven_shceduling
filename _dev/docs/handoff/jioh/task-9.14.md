# Handoff — task 9.14 Consumer rework (2026-10-10, ~21:20 KST) — complete

Branch `jioh/dataset-rebuild` (Phase 9 works on this branch only, `_dev/` included), pushed through `a473070d`; the harness changelog entry (2026-10-09, 9.14) is the last commit, as spec decision 14 says. Spec `_dev/docs/spec/jioh/task-9.14-consumer-rework.md` (14 decisions, decision 2 amended); changelog `_dev/research/jioh/task-9.14-consumer-rework/changelog.md` (D1–D14, the decision-11 hand-off table); facts `reads.md` (R1–R4). Use `python3.12` (3.12.4); the default `python3` is 3.13 without `jsonschema`, and `make -C dataset …` needs `PY=python3.12`.

## What landed on 2026-10-10 (D10–D14)

- **The trace replay** (D10): the compiler's `replay` param (`wakes`, `cycles`, `runs` streams; a seeded window per measured or periodic task, a batch job from its start; operations and keystrokes as compiled; a short or wrong-kind stream fails the build); `dataset/tools/meas/replay_fold_in.py` and the six streams under `dataset/replay/` (byte-stable, `--check`); the batch repeats by the Q6 rule — MNIST's sixth, the upgrade's fourth (`reads.md` R1, R2).
- **The variants** (D12): all nine sets, 78 artifacts, `dataset/build.variants.manifest.json` committed and pinned (`pins.variants.all` `2a8893a9…`); `variants.py --check` verified.
- **Three harness fixes the rebuilt set forced**: a variant file is scored on its base's terms with its windows on its own segments (D11, `scoring.with_variants`); the runner aggregates each run as it is built (D13); the hog test and the CPU-since reading by bisection (D14). Outputs unchanged, fixture tests byte-identical.
- **Docs in scope**: `docs/workload/building-plan.md` §5a and the slice workflow's CI note per decision 4; the gate spec's replay statements name the window and repeat rules.

## Verification (all local; the three CI workflows run on pushes to `main` alone)

`make -C dataset lint` clean (41 min); dataset suite 464 passed, 1 skipped (50 min); `make -C dataset check` verified (51 artifacts); `variants.py --check` verified (78); `make -C harness lint` clean; harness suite green (274 + the three restated, the pipeline tests rerun on D13); `make -C harness smoke` green on D13 + D14 — 196 runs, 4 h 50 min, `c6-dual` about three hours of it.

## Open for the next tasks (every item also on the TODO's 9.15 / 9.16 / Phase 10 lines)

- Phase 10: the RQ0 run's cost on `c6-dual` — about 40 min per run for the records build alone (42 million trace lines), 100 `random` seeds planned; a cheaper records path is a task of its own. The Layer-1 and RQ4 items (decision 11) per the changelog's hand-off table.
- 9.15: the hand-offs of D1–D10 (the TODO line); the stream directories (`dataset/stimulus/`, `launch/`, `replay/`) undescribed in `docs/`.
- 9.16: the reproductions named per entry (`--check` of the streams and the variants, the repeat tables, the pins' hashes).

## Facts worth not rediscovering

- The raw landings for the six streams come from `gh release download` (about 4 GB); the tool wants them as `<raw-root>/<release>/<landing>` as the asset unpacks (`SOURCES` in `replay_fold_in.py`).
- `runs/smoke/` holds the smoke's 196 runs (the invocations cached under `runs/.cache`); a rerun rebuilds records from the cache.
- The scoring spec, guard spec, prior table and dataset manifest hashes did not move since D7; only the variants pin was filled.
