# Handoff — Phase 6: 6.1 and 6.2 done, 6.3 picked up

Written 2026-09-09. Repo `LLM_driven_shceduling`, branch `jioh/driver-table-v0` (off `main` after PR #4; `_dev/` edits land on this branch by the user's call). Local commits not yet pushed at handoff time (`git log origin/jioh/driver-table-v0..HEAD`).

## Where things stand

- **Phase 6 `[WIP]`**, spec `_dev/docs/spec/jioh/phase-6-driver-table-v0-and-scoring-spec.md`. Order 6.1 → 6.2 → 6.3 → 6.4.
- **6.1 Switch overhead — done.** Lane-time `switch_window`, `hogs` column, config schedule as third input, `check_mlfq_levels.py`, `mock-switch`. All switch semantics settled with 인경민 on 2026-09-09 (memo §5/§7; metrics doc §11 items 7–9).
- **6.2 Scoring spec — done.** `harness/scoring/scoring-spec.yaml` (23 files, 44 terms), schema, lint (`tools/harness/scoring.py`, `tools/scoring_lint.py`, in `make lint`), 20 tests; harness CI builds the coreset first (`make -C dataset dataset`). 83 harness tests, lint clean.
- **6.3 Prior table — `[WIP]`, not started.** Next: brief from spec decisions 1–2 and 4, then straight to authoring (test-first for any code; the table is data).
- **Mocks follow the guide's MLFQ rules and the memo** (fixtures README item 7).

## 6.3 inputs

- Contract: `docs/data-contracts.md` §10 (prior table: exactly one entry per row, `basis: theory`, a justification sentence on the row and on the entry; 32 rows keyed `(mode, background_wanted)`; per-row `batch_bandwidth_cap` null or 0.05–0.95, `default`).
- Machine schema and lint: `daemon/driver-table/schema/driver-table.schema.json`, `daemon/tools/drivertable/{config_schema,lint}.py`; `make -C daemon lint` looks for `daemon/driver-table/*.yaml`. Config schema: 16 modes; MLFQ `num_queues` 2–8 (3), `timeslice_us` 500–100000 (2000), `timeslice_growth` 1–8 (2), `boost_interval_us` 10000–10000000 (100000); EDF `residual_timeslice_us` 500–100000 (2000); LOTTERY `batch_share` 0.01–0.90 (0.15) ≤ cap, `timeslice_us`; FIFO no params.
- Spec decisions: all 32 rows `basis: theory`, one sentence each on row and entry; any of the four algorithms by theory; references ids only where they already exist (`ostep`, `waldspurger-osdi94`); no new sources.
- Rows the coreset exercises (17): browsing/T, compile/T, dev/T, gaming/T, gaming/F, idle/T, indexing/F, mail/T, media/T, meeting/T, ml-train/T, office/T, photo/T, render/T, backup/T, transcode/T, video-edit/T. The pair review (6.4) will compare the 16 same-mode pairs and the three C2 row-pairs (`ml-train/T`–`indexing/F`, `gaming/T`–`gaming/F`, `render/T`–`backup/T`); a row's justification should name the scored term it serves (scoring spec).
- Mode semantics: `docs/recognition-vocabulary.md` §1; boot default provenance §2.
- Scoring terms per file: `harness/scoring/scoring-spec.yaml`.

## Rules of this project the session must keep

- Archives only on explicit request (`CLAUDE.md`). Do not propose or announce one.
- One question per message in grills; plain chat, no AskUserQuestion.
- Nothing enters code or docs that is not a field or rule in the contracts, the metrics doc, or the spec.

## Environment

- venv in the session scratchpad: `pip install -r dataset/tools/requirements.txt -r daemon/tools/requirements.txt -r harness/tools/requirements.txt`; pass `PY=<venv>/bin/python` to the Makefiles. The harness lint needs `make -C dataset dataset` once.

## Carried forward (not 6.3's)

- 박이안 on the repeat index; `c1-media` tier-1 familiarity annotation; C1-derived `demand: calibration`; gate spec items (Phase 7).
