# Phase 2 — Workload dataset generation

Builds steps 1–4 of the adopted build order (docs/workload/building-plan.md §5) plus a closing repo-handoff sub-task. Parent: `## Phase 2` in `_dev/TODO.md`; decision session: this spec's grill (2026-08-27).

## Scope

- `dataset/archetypes.yaml` v0.1, the canonical JSON Schema, the timeline→canonical compiler with lane-scaling pass + linter + invariant tests, and the core timelines compiled to `coreset-single`/`coreset-native`.
- The meas-ci measurement campaign: workflows, runs, and the parameter fold-in replacing the `meas-pending` placeholders.
- Repo prep + onboarding docs so teammates can start their own work areas.
- Outside the phase: simulator Phase 0, RQ0 gate, naturalistic generator.

## Locked decisions

### 1. Phase boundary

Phase 2 ends at build step 4: the authored timelines and their compiled canonical coreset, checked statically (linter, provenance, invariants, demand estimate) but not executed — the first end-to-end run is step 5's integration test, in a later phase. The meas-ci campaign runs inside the phase (amended 2026-08-27): its results land during Phase 2 so the coreset ships on measured numbers, with only the RQ0-gate revisit remaining.

### 2. Sub-task set and ordering

Five sub-tasks: **2.1** `dataset/archetypes.yaml` v0.1 (12 entries per archetype-plan §4–§5; `meas-pending` placeholders allowed; `modeling_notes` from day one, including the two decided binding notes) — **2.2** canonical JSON Schema (machine form of interpretation-contract §4) — **2.3** timeline→canonical compiler + lane-scaling pass + linter + invariant tests — **2.4** core timelines: ~6 novel designs + derivation scripts → ~24 files compiled to both modes; coverage-grid fill happens here — **2.5** repo prep + onboarding docs — **2.6** meas-ci campaign: the three workflow families (headless CLI, Xvfb GUI, name verification), N runs with spread, and the analysis folding measured parameters into `archetypes.yaml` in place of the `meas-pending` tags. Order: 2.1 ∥ 2.2 (parallel-eligible) → 2.3 → 2.4 → 2.5 last; 2.6 runs parallel from any point, with its fold-in landing before 2.4's final compile and sign-off.

### 3. Timeline-format ownership split

The base timeline format (what the compiler parses) is fixed in 2.3's own spec session; the authoring sugar (`variants:`/`inherit()`/`inject:`, consumed by the derivation scripts) is fixed in 2.4's.

### 4. CI wiring in 2.3

The linter and invariant tests are wired into GitHub Actions as part of 2.3's deliverable, not left local-only.

### 5. Static demand estimate

The compiler emits a per-file aggregate CPU-demand estimate for `-single` output; 2.4's files must land in the ~100–150% lane window by that estimate. The RQ0 admission test remains the real enforcement of the demand budget; files may still be redesigned at the gate.

### 6. Handoff sub-task scope

2.5 covers onboarding docs (per-teammate reading paths) plus repo working-structure prep for collaboration. Its exact contents are left to its own session.

## Open items

- Sub-task-internal design (compiler tooling, base timeline syntax, sugar syntax, coverage-grid fill, onboarding contents) is deliberately left to each sub-task's own session.
