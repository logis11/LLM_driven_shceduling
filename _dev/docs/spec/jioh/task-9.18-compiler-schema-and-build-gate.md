# Task 9.18 — Compiler, schema and build gate

The three class-A process findings of the 2026-10-10 dataset audit (`_dev/docs/audit/jioh/2026-10-10-dataset-audit-before-9.15.md`: A1 the counterparts' keystroke slice, A2 the timelines' bound values without a source field, A4 the build-gate holes) and the dataset test suite's time handed from 9.17. Decided in the 2026-10-11 grill. Parent: `_dev/TODO.md`, (jioh, 9.18); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`.

## Scope

- The compiler rule that makes a derived file's keystrokes its base's, over the slice the derived file keeps; the test that states it.
- The `source` field on every value a timeline binds, with its lint; the twelve measured values and the design values tagged from `_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md`.
- The build gate: the variants check in the gate, the on-disk build verified against the manifests, the compiler and the streams pinned in the manifest, one Linux CI run.
- The `coreset` test fixture reading the blessed build.
- The rebuild, re-bless and re-pin the field and the rule force, with every document whose sentences or numbers the rule changes.

## Locked decisions

### 1. A derived input window names the stream window it is a slice of

An input window may carry the window of which it is a slice: that window's `from`, `to` and index in its file's input list. The compiler draws the stimulus offset for the outer window — by its length and its index — and places inside the slice the keystrokes that fall in it, so a counterpart's keystrokes are byte-identical to its base's over the slice. A window carrying no outer window is its own. The field is compile-time: the canonical workload and its schema do not change.

### 2. The deriver writes the field

When a variant op replaces the input list, a new window lying wholly inside one of the base's input windows of the same task is written with that base window as its outer window. A window inside none is written without one. The author's variant spec does not restate the base's windows.

### 3. The test is a subset relation

For every interactive counterpart, the counterpart's input wakes are a subset of its base's input wakes in the counterpart's span. Equality is not asserted: the counterpart's operations sit at their own positions (9.10 D44), and the compiler drops the keystrokes that fall inside an operation.

### 4. `source` is a map beside `bind`

Each task carrying a `bind` carries a `source` map with the same keys. A value is one source tag, a list of source tags, or one of the labels `design`, `convention`, `arithmetic`. Tags are checked against `dataset/sources.yaml` as the library's are; labels are not registry entries. Variant ops that write a `bind` write its `source`. The reason behind a design label stays in `bound-values.md` and the timeline's comment.

### 5. The manifest pins the compiler and the streams by content

`build.manifest.json`'s `inputs` gains the compiler's source files and the stimulus and replay streams, each as path → SHA-256 of its bytes, as the archetype library and the schema are pinned today.

### 6. `check` verifies the on-disk build

`make check` is: derive drift, the dataset recompile against `build.manifest.json`, the variants rebuild against `build.variants.manifest.json`, and `build/` equal to the two manifests — every file in `build/` matching an entry, every entry present, no file in neither. A missing `build/` fails. `dataset.yml` builds the dataset and the variants before it checks. The harness workflows run the dataset check after their build step.

### 7. The dataset workflow gains a manual trigger

`dataset.yml` gains `workflow_dispatch`. One run on this branch, on Linux, compiles the blessed manifest; its run id is recorded in the sub-task changelog. The run is started on 인지오's confirmation.

### 8. The compile report is a blessed artifact

The compiler writes each artifact's report beside it in `build/`, and the manifest pins the reports' hashes in a section of their own; the `demand` section is unchanged. The `coreset` fixture reads an artifact and its report from `build/` when both hash to the manifest's entries, and compiles otherwise. The variants write no report.

### 9. The documents the rule falsifies are corrected in this sub-task

`docs/daemon/prior-table-pair-review.md` findings 8 and 10 and its counterpart table's keystroke counts, the scoring spec's `c7-mail` comment, and the RQ0 gate spec's input-wake-count line are restated to the mechanism and the rebuilt numbers; the pinned ones are re-pinned.

## Invariants

- An input window lies inside the outer window it names; the index names an existing window of that list.
- A shifted variant of a derived file keeps its outer windows shifted with it.
- `bind` and `source` have the same key set on every task.
- The `source` field changes every timeline blob, so every artifact and every variant is rebuilt, re-blessed and re-pinned in this sub-task: the dataset manifest, the variants manifest and the scoring spec pins in the RQ0 gate spec, and the harness's build-dependent fixtures.
