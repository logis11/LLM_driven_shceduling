# Handoff — start of Phase 7 (coreset attribute coverage), carrying Phase 6's results

Written 2026-09-09 at the close of Phase 6. For a fresh session that will pick up **Phase 7 — Coreset attribute coverage** in `_dev/TODO.md` (인지오's section). Repo `LLM_driven_shceduling`.

## Where things stand

- **Branch**: Phase 6 was done on `jioh/driver-table-v0` (the user's call: `_dev/` edits land there). Pushed at handoff time; no PR open. Check `git log main..jioh/driver-table-v0` and GitHub before branching. Precedent: PR against `main`, merged by the user (PR #3 Phase 4, PR #4 Phase 5); Phase 6's PR is the natural next step, then Phase 7 on a new branch off `main` (the user names branches).
- **Phase 6 is `[done]`** (6.1–6.4). **Phase 7 is fresh**: no spec, no `[WIP]`. `daily-work-harness:pick-up-task` routes it to the spec track: grill → `grill-to-spec` → inline `7.M`. Phases 8 (harness upper half) and 9 (integration) were renumbered from 7 and 8 today; every live doc reference moved with them.
- **No archive was written for Phase 6.** Archives are written only when 인지오 says so (`CLAUDE.md`). Do not propose one.

## What Phase 6 produced (do not re-derive)

- **Switch overhead (6.1)**: `switch_window` primitive, lane-time window (closes when the last hog has received `W_single` of CPU since `t_apply`), `hogs` twentieth records column, config schedule as the harness's third input, `harness/tools/check_mlfq_levels.py`, fixture `mock-switch`. Switch semantics all settled with 인경민 (memo `docs/memos/2026-09-08-algorithm-switch-semantics-for-the-simulator.md` §5/§7; metrics doc §11 items 7–9).
- **Scoring spec (6.2)**: `harness/scoring/scoring-spec.yaml` (23 files, 44 terms), schema, lint in `make -C harness lint` (needs `make -C dataset dataset` once), 20 tests. Terms: `ready_wait` P99, `job` miss rate, progress, makespan; C2 windows 60 s–`T_end`; derived files carry their base's terms verbatim with `base` declared.
- **Prior table (6.3)**: `daemon/driver-table/prior.yaml`, 32 rows; algorithm by mode (EDF gaming/media/meeting; LOTTERY wanted batch; MLFQ interactive, idle, unwanted batch; FIFO nowhere), cap by attribute derived from the scoring weights (1/3, 1/2, 1/5; 0.05 floor unwanted; 1/2 stated assumption where no batch term exists), boot params, `sources` ids on every row and entry (schema + lint; `liu-jacm73` verified and added). Spec decision 2: every judgement rests on a reference.
- **Pair review (6.4)**: `docs/daemon/prior-table-pair-review.md` (record). No defect. Findings: (1) the cap is inert on `c2-p2a`'s download — kept, p2 tests the attribute in one direction; (2) fourteen of 32 cells have no coreset instance because the grid tool lacks the `background_wanted` axis — the reason Phase 7 exists; (3) one author, stated limitation, no second reader.
- **Batch-class rule memo** to 인경민: `docs/memos/2026-09-09-batch-class-rule-for-the-simulator.md` (rules B1/B2, worked examples, action plan). No reply yet.

## Phase 7 inputs

- The TODO line for Phase 7 states the scope: attribute axis in the coverage grid (`dataset/tools/wlc/grid.py` counts mode × tier today; `dataset/coverage-grid.json` is its committed output), a derived family of `false` files for the interactive modes from their C1 bases (C4's injection machinery in `dataset/timelines/coreset/*.variant.yaml`, plus a segment patch flipping the label), the all-32-cells requirement for the generalset, manifest, building plan §3 family list, dataset-design table, study guides; downstream a scoring-spec entry per new file (`base` declared, base's terms verbatim; `harness/tools/tests/test_scoring.py::test_every_coreset_file_but_idle_has_terms` will fail until added) and the pair review's sentences for the newly exercised rows.
- Facts verified 2026-09-09: coreset `ground_truth` exercises 17 legal cells; only `gaming/false` (`c2-p2b`) and `indexing/false` (`c2-p1b`) are `false`; `meeting/true` appears only in `c6-fold`. Attribute accuracy on this coreset is near-degenerate (always-`true` scores ≈ 95 %).
- Design questions for the grill (not pre-decided): which modes get a `false` variant (the interactive-only six, or every mode with a C1 base), what the injected unwanted job is per mode (CPU-bound, so the cap acts; archetype and name choice), whether the family is a new C-group or an extension of C4, demand-class declaration for the new files (Phase 3's inherited `demand: calibration` issue), how the grid's new axis is reported in the paper's dataset table.

## Rules of this project the session must keep

- Archives only on explicit request. One question per message in grills; plain chat. Never cite a document section without saying what it says. Judgements and numbers rest on references; propose a source to add rather than asserting.
- Nothing enters code or docs that is not a field or rule in the contracts, the metrics doc, or the spec.

## Environment

- venv in the session scratchpad: `pip install -r dataset/tools/requirements.txt -r daemon/tools/requirements.txt -r harness/tools/requirements.txt pypdf`; pass `PY=<venv>/bin/python` to the Makefiles. `make -C dataset dataset` before `make -C harness lint`.

## Carried forward (not Phase 7's)

- Replies: 인경민 on the batch-class memo; 박이안 on the repeat index.
- Phase 8 pre-registration items: p2a's gap read as mode recognition; the fourteen unmeasured cells as "not measured"; `random` draw definition and seed count; boot-default sensitivity pair; `c1-gaming` separate line; guard exemptions.
- `c1-media` tier-1 familiarity annotation; C1-derived `demand: calibration`; the word "familiarity".
