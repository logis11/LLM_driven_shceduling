# Handoff — Phase 6: 6.1–6.3 done, 6.4 picked up

Written 2026-09-09. Repo `LLM_driven_shceduling`, branch `jioh/driver-table-v0` (off `main` after PR #4; `_dev/` edits land on this branch by the user's call). Local commits not yet pushed at handoff time (`git log origin/jioh/driver-table-v0..HEAD`).

## Where things stand

- **Phase 6 `[WIP]`**, spec `_dev/docs/spec/jioh/phase-6-driver-table-v0-and-scoring-spec.md`. Order 6.1 → 6.2 → 6.3 → 6.4.
- **6.1 Switch overhead — done.** Lane-time `switch_window`, `hogs` column, config schedule as third input, `check_mlfq_levels.py`, `mock-switch`. All switch semantics settled with 인경민 on 2026-09-09 (memo §5/§7; metrics doc §11 items 7–9).
- **6.2 Scoring spec — done.** `harness/scoring/scoring-spec.yaml` (23 files, 44 terms), schema, lint (`tools/harness/scoring.py`, `tools/scoring_lint.py`, in `make lint`), 20 tests; harness CI builds the coreset first (`make -C dataset dataset`). 83 harness tests, lint clean.
- **6.3 Prior table — done.** `daemon/driver-table/prior.yaml`: 32 rows, algorithm by mode (EDF gaming/media/meeting; LOTTERY wanted batch; MLFQ interactive, idle, unwanted batch; FIFO nowhere), cap by attribute derived from the scoring weights (1/3, 1/2, 1/5; 0.05 floor unwanted; 1/2 stated assumption for wanted rows with no batch term), boot params, `sources` ids on every row and entry (`liu-jacm73` added and verified). Schema + lint carry `sources`; contract §10 changelog 2026-09-09. Spec decision 2 amended: every judgement rests on a reference. `make -C daemon lint` clean, 28 tests.
- **6.4 Pair review — `[WIP]`, not started.** Spec decisions 3–4: the 16 same-mode pairs and the three C2 row-pairs; one sentence per pair naming the knob, the scored term it moves, and agreement with the scoring weights; a pair without a sentence is a table defect fixed in 6.3's file. Open at pickup: where the sentences live now that archives are written only on request.
- **Mocks follow the guide's MLFQ rules and the memo** (fixtures README item 7).

## 6.4 inputs

- The table: `daemon/driver-table/prior.yaml` (its header states the rules each row follows).
- The scoring terms per file: `harness/scoring/scoring-spec.yaml` (weights the review checks direction against).
- Which files exercise which rows: 17 rows — browsing/T, compile/T, dev/T, gaming/T, gaming/F, idle/T, indexing/F, mail/T, media/T, meeting/T, ml-train/T, office/T, photo/T, render/T, backup/T, transcode/T, video-edit/T. C2 row-pairs: `ml-train/T`–`indexing/F` (p1), `gaming/T`–`gaming/F` (p2), `render/T`–`backup/T` (p3).
- Lint already guarantees no same-mode pair composes byte-identical; the review is the judgement on top.

## Rules of this project the session must keep

- Archives only on explicit request (`CLAUDE.md`). Do not propose or announce one.
- One question per message in grills; plain chat, no AskUserQuestion.
- Nothing enters code or docs that is not a field or rule in the contracts, the metrics doc, or the spec.

## Environment

- venv in the session scratchpad: `pip install -r dataset/tools/requirements.txt -r daemon/tools/requirements.txt -r harness/tools/requirements.txt`; pass `PY=<venv>/bin/python` to the Makefiles. The harness lint needs `make -C dataset dataset` once.

## Carried forward (not 6.3's)

- 박이안 on the repeat index; `c1-media` tier-1 familiarity annotation; C1-derived `demand: calibration`; gate spec items (Phase 7).
