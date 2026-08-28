# Task 2.4 — Core timelines

Fixes the derivation mechanism, grid mechanics, and authoring conventions for the ~24-file core set. Parent: `2.4` in `_dev/TODO.md`; phase spec: `_dev/docs/spec/phase-2-workload-dataset-generation.md`. The file inventory itself (C1×6, C2 3 pairs, C3×3, C4×3, C5×3, C6×3) is normative in docs/workload/building-plan.md §3 and is not re-decided here.

## Scope

- The ~6 novel base timelines, the variant specs deriving the rest, the generic deriver, the coverage-grid report, and the compiled coreset (`-single`/`-native`).
- Final compile and demand-window sign-off wait for the meas-ci cli:2 fold-in (phase spec §1).

## Locked decisions

### 1. Derivation: declarative variant specs + one generic deriver

Novel timelines are plain base-format files; each derived file is a small yaml variant spec (`from: <base>` plus a closed set of ops — replace-task, add-task, rename, set-meta, …) executed by a generic deriver inside `make dataset`. The building plan's named sugar maps onto it: `inherit()` = `from:`, `inject:` = an add-task op, `variants:` = several outputs of one spec. The C2/C4/C5 disciplines are structural: a derived file provably differs from its base by exactly its ops.

### 2. Coverage grid: annotation-driven, generated

Segments gain an optional `familiarity:` annotation (tier 1–5) beside `scenario:` — compiler-ignored, linter-read; unannotated segments default to tier-by-name lookup. The grid (domain × familiarity, counted in segments) is emitted mechanically from the annotations across all core timelines as a generated committed artifact — the paper table derives from the files it describes and cannot drift. Hole sign-off stays human (building-plan §9.2).

### 3. Duration and demand-class conventions

Default segment length 120 s; C1 single-segment files 60 s. Demand classes: C1 = `calibration`; C2–C6 default `oversubscribed` (hard-checked 100–150%), any per-file exception a visible authored declaration.

### 4. Seed policy

Each novel base timeline carries a distinct fixed committed seed. Variant specs inherit the base seed and never override it silently — the deriver warns on an explicit override, since a changed seed defeats the paired byte-discipline the derivation exists to provide.

### 5. Name strings

Bind per the scenario catalog with the meas-ci names-table confirmations recorded (`soffice.bin`, live `cc1`, plain `updatedb`); no re-decisions.

## Open items

- Coverage-grid hole sign-off happens at 2.4 wrap-up, on the generated report.
- Final compile + sign-off blocked on the cli:2 fold-in (supersession rule: all cli params re-point to cli:2).
