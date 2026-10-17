# Task 9.22 — Build time

The dataset gate's redundancy and the two slow steps of a build, so that one CI run compiles the set once; decided in the 2026-10-11 grill after 9.18's verification run (`_dev/research/jioh/task-9.18-compiler-schema-and-build-gate/changelog.md` D7). Parent: `_dev/TODO.md`, (jioh, 9.22); phase spec `_dev/docs/spec/jioh/phase-9-workload-dataset-rebuild.md`.

## Scope

- `make check`, `make lint` and the dataset workflow, with one compile per run.
- The canonical schema validation's implementation.
- The compile and the variants parallel over files.
- The two tests that recompile or re-validate the set.
- The build's time measured before and after, on the home machine and in one CI run.

## Locked decisions

### 1. The build step proves reproducibility; `check` compares

`make dataset variants` rewrites the two manifests; `make check` is derive drift, both manifests equal to their committed bytes, and `build/` equal to the manifests. The in-memory recompile flags of `compile.py` and `variants.py` remain for independent verification and leave the gate. The workflow runs the build, then the tests, then the check.

### 2. `lint` is the pre-compile check

`make lint` is the repo, timeline and bound-value lints alone. The canonical lints are the compiler's, run on every artifact as it is built, as today.

### 3. The schema validation runs on `jsonschema-rs`

The canonical lint validates against the unchanged workload schema with `jsonschema-rs`, a dependency of the dataset tools. The schema and the validation's meaning do not change.

## Invariants

- No artifact or report byte changes: the sampling, the canonical form and the compile's output are untouched, and the gate's statement — the committed manifests are what a recompile writes — is unchanged in meaning. The manifests' `inputs` pin the compiler's sources by content (9.18 decision 5), so the compiler change re-blesses both manifests and re-pins the RQ0 gate spec, the artifacts identical.
- The tests that read the set follow 9.18 decision 8: the blessed build when the hashes match, a compile otherwise.
- The measurements before and after are recorded in the sub-task changelog.
