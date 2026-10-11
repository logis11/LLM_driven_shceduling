# Task 9.18 — changelog

One entry per change applied in the sub-task (`dataset/`, `.github/workflows/`, `harness/`, the docs): what changed, old state, new state, the decision it applies (spec `_dev/docs/spec/jioh/task-9.18-compiler-schema-and-build-gate.md`), commit. Each entry names what it hands to 9.15 or 9.16.

## D1 — the slice rule: a derived keystroke window is its base's (2026-10-11)

Spec decisions 1–3; audit A1, option (ii). Old state: the compiler drew every input window's stimulus offset as `uniform(seed, iid, "stimulus", j) × (span − window length)`, so a counterpart's 22.385 s window and its base's 56 s window drew different offsets under the same seed and shared no keystroke timestamp (the audit's table: browsing 0 of 29, office 0 of 103, dev 0 of 78 shared). New state: an input window may carry `slice_of: {from, to, index}`, the stream window it is a slice of (`dataset/tools/wlc/timeline.py`: within it, a non-negative index); the compiler draws the offset for that window — its length, its index among the task's windows — and adds the slice's lead inside it (`compiler.py`), so the slice's keystrokes are the base's over the same instants. The deriver writes the field on `set-input`: a new window wholly inside one of the base's windows of the same task takes that window and its index among the task's windows in time order; a window inside none is its own; an authored `slice_of` stands (`deriver.py`, `_sliced`). The segment-length shift moves a slice's outer window by the slice's own displacement (`variants.py`). The twelve `set-input` windows of `c7.variant.yaml` re-derive with `slice_of: {from: 2s, to: 58s…, index: 0}`; the variant spec is unchanged. The canonical workload and its schema are unchanged in shape.

Sanity before the rebuild (the 9.17 build's compiler on the new timelines, `single` mode): browsing — the base 118 input wakes, the counterpart 79, the base's in [0, C) 85, shared 79; office — 249, 91, 102, 91; mail — 33, 0, 0, 0. The counterpart's wakes are the base's over the slice less those inside the counterpart's own operations (9.10 D44 places them at the counterpart's positions; the compiler emits no keystroke inside an operation), hence the subset relation and not equality.

Tests: `test_coreset.py::test_c7_input_wakes_are_a_subset_of_the_bases_in_the_first_c_seconds` (the six counterparts that keep a keystroke window; browsing, office and dev non-empty; mail empty), `test_set_input_writes_the_bases_window_as_slice_of`, `test_every_counterpart_keystroke_window_is_its_bases_slice`, `test_segment_shift_moves_a_slice_with_its_window`; `test_lint.py`'s three `slice_of` rules.

Hands to 9.15: `dataset/README.md`'s C7 row and the building plan's C7 text ("one-diff pair") read against the mechanism.

## D2 — the bound values' `source` map (2026-10-11)

Spec decision 4; audit A2; 9.10 D32. Old state: a timeline's `bind` values and `count` carried no provenance; the grounding lived only in `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md`. New state: a task carrying `bind` or `count` carries a `source` map with the same keys — a registry tag, a list of tags, or one of the labels `design`, `convention`, `arithmetic` (`BOUND_LABELS`); `dataset/tools/wlc/linter.py::lint_bound_sources` checks the key sets both ways and every tag against `dataset/sources.yaml` with the library's `_check_tag`; `lint.py` runs it on every timeline. The loader carries the map without checking it (`timeline.py`), as the library class carries its tags and `lint_repo` checks them. The 23 base timelines and the five variant specs' `add-task`/`patch-task` ops tagged from `bound-values.md`: the twelve measured values (`meas-ci:background:2026-09-19` … `2026-10-04`, `meas-ci:build:2026-09-18`, `meas-ci:desktop:2026-10-04`, `lavd-ossna24:s16`, with `pytorch-examples`, `kdenlive` and `glam` beside the campaigns that measured them), the design values labelled `design` (`parallelism_cap: 8`, the chain's `lane_share`, `c6-spoof`'s batch job, `c4-office`'s 6 s archive). `count: 4` on the hidden tabs (`c1-browsing`, `c1-office`, `c3-workday`, `c3-evening`, and `c4-compile`'s injected renderers) takes `[glam, meas-ci:desktop:2026-10-04]`. The spec's decision 4 is amended to name `count` among the bound values, as D32 does.

`dataset/sources.yaml` gains `pytorch-examples`, `kdenlive` and `glam` (type `deployed-system`; their `docs/references.md` entries exist since 9.10): the timelines now derive from them, which the registry's own rule asks. Every artifact's bytes change through `meta.derived_from`.

Tests: `test_lint.py::test_real_timelines_bound_values_are_sourced`, `test_bound_values_carry_a_source_tag_or_a_label` (13 cases).

Hands to 9.16: `bound-values.md` and the timelines' `source` maps agree entry for entry (the lint checks form, not that each tag is the right ground).

## D3 — the manifest pins the compile's inputs and the reports (2026-10-11)

Spec decisions 5, 8. Old state: `build.manifest.json.inputs` pinned `archetypes.yaml` and the workload schema; the compile report (duration, demand per task and per segment, operations, replay) existed only in memory, its rounded extract under `demand`. New state (`dataset/tools/compile.py`): `inputs` is path → SHA-256 for the library, the schema, `compile.py`, `wlc/*.py`, `stimulus/*.jsonl` and `replay/*.json.gz` (`input_files`); each artifact's report is written beside it as `<id>.report.json` (`report_bytes`: sorted keys, two-space indent) and pinned under a new `reports` section; `demand` is unchanged. The variants write no report.

Tests: `test_manifest.py::test_manifest_records_demand_per_artifact` (the reports' hashes), `test_manifest_pins_the_compile_inputs_by_content`.

## D4 — `check` verifies the on-disk build; the workflows (2026-10-11)

Spec decisions 6, 7. Old state: `make check` was derive drift plus the in-memory recompile against the manifest; `variants.py --check` ran nowhere; `harness.yml` and `harness-smoke.yml` built the variants in write mode and read whatever came out; `dataset.yml` ran on `push: main` and pull requests only. New state: `dataset/tools/check_build.py` — `build/` equals the union of the two manifests (every file pinned by one, every pin present, every hash equal; a missing `build/` fails); `make check` is derive drift, `compile.py --check`, `variants.py --check`, `check_build.py`; `dataset.yml` runs `lint`, `dataset`, `variants`, `test`, `check` and gains `workflow_dispatch`; the two harness workflows run `make -C dataset check` after their build steps. Tests: `test_check_build.py` (three cases).

## D5 — the `coreset` fixture reads the blessed build (2026-10-11)

Spec decision 8; the 9.17 hand-off (TODO 9.18 (d)). Old state: `test_coreset.py`'s module fixture recompiled the 51 timelines in-process, about 25 of the suite's 50 minutes. New state: for each timeline the fixture reads `build/<set>-single/<id>.workload.json` and its report when both hash to the manifest's `artifacts` and `reports` entries, and compiles otherwise (`_blessed`). A run after `make dataset` costs the tests alone.
