# Task 9.22 — changelog

One entry per change applied in the sub-task (`dataset/`, `.github/workflows/`, the docs): what changed, old state, new state, the decision it applies (spec `_dev/docs/spec/jioh/task-9.22-build-time.md`), commit. The measurements before and after close the sub-task.

## Before (2026-10-11, 9.18 D7, the home machine — M1 Pro, Python 3.12)

| step | time | what it compiled or validated |
|---|---|---|
| `make lint` | ~42 min | the 51 timelines compiled in memory (24) and schema-validated (18) |
| `make dataset` | 22–24 min | the 51 artifacts, serial, each schema-validated |
| `make variants` | 33–35 min | the 78 variants, serial |
| `make test` | 44 min | `test_manifest` recompiling the set (23), `test_no_file_fails_on_its_demand` re-validating it (19) |
| `make check` | 56–59 min | the set recompiled (24) and the variants rebuilt (35) in memory against the manifests |

One CI run of `dataset.yml`: about 3.5 h on the home machine's figures; the schema validation at about 0.6 MB/s (`c6-dual` 188 MB in 335 s).

## D1 — the gate compares; the build proves (2026-10-11)

Spec decision 1. `make check` was derive drift, `compile.py --check`, `variants.py --check`, `check_build.py`; it is derive drift and `check_build.py`, which now also compares each manifest on disk with its bytes at `HEAD` (`check_committed`: `git show HEAD:<path>`). The build step rewrote the manifests, so equality states that the recompile reproduces the committed set — the same statement the in-memory flags made at twice the compile. The two `--check` flags remain for independent verification and leave the gate; the workflow's order is unchanged (`lint`, `dataset`, `variants`, `test`, `check`).

## D2 — `lint` before the compile (2026-10-11)

Spec decision 2. `lint.py` ran the repo lints, the timeline lints and then compiled every timeline in memory to run `lint_canonical`; the compile already runs the same `lint_canonical` with the same arguments on every artifact it writes and fails on an error, so the pass repeated the build's check. `lint.py` is the repo and timeline lints (the bound values' sources among them); seconds.

## D3 — `jsonschema-rs` (2026-10-11)

Spec decision 3. `wlc/linter.py` validated with `jsonschema.Draft202012Validator(schema).iter_errors`; it validates with `jsonschema_rs.validator_for(schema).iter_errors`, the validator compiled once per schema document per process, the error lines in the same form (`schema: <message> at <instance path>`). Measured on `c7-transcode` (95 MB): `jsonschema` 141 s, `fastjsonschema` 19.7 s (draft-07 package; passed on this schema but outside its stated support), `jsonschema-rs` 1.4 s, a malformed event caught by each. `requirements.txt`: `jsonschema>=4.20` → `jsonschema-rs>=0.29`. The schema is unchanged.

## D4 — the compile and the variants parallel over files (2026-10-11)

Spec scope. `compile.py`: `compile_one(root, path)` compiles one timeline in every mode (the library and the schema loaded once per worker process), `build_all` maps it over a `ProcessPoolExecutor` of `--jobs` workers (default the CPU count) and sorts the results, so the manifest bytes are those of the serial build. `variants.py`: the (set, file) pairs (`wlc.variants.jobs_of`) each build in a working directory of their own (`build_job`) over the same kind of pool, the results re-ordered to spec order. `test_manifest.py` reads the blessed build when every artifact and report hashes to the committed manifest (9.18 decision 8's rule) and compiles otherwise.

## D5 — the manifests re-blessed, the gate re-pinned (2026-10-11)

Spec invariant. The compiler's sources are inputs the manifest pins by content (9.18 decision 5), so the three changed files (`compile.py`, `wlc/linter.py`, `wlc/variants.py`) change `build.manifest.json`'s `inputs` and, through it, the variants manifest's; every artifact, report and variant is byte-identical to the 9.18 build (the diff of the two manifests against `HEAD` is the `inputs` section alone). Pins: dataset manifest `d10bcd42a31ea0617133bccf739941ecf347dab296c68a5ab5bc6a4000377d4d`, variants manifest `831a854ebcd23c0047e710a04ee6851478924a96b6320e4a91ca1d368c9ba0b8`; the RQ0 gate spec carries both; `harness/CHANGELOG.md` has the entry.

## After (2026-10-11, the home machine — M1 Pro, 10 cores, Python 3.12)

| step | before | after |
|---|---|---|
| `make lint` | ~42 min | 0.8 s |
| `make dataset` | 22–24 min | 52 s |
| `make variants` | 33–35 min | 1 min 46 s |
| `make test` | 44 min | (measured below) |
| `make check` | 56–59 min | 1.7 s |

The compile's 24 minutes were mostly the schema validation (18 of them, by 9.18 D7's measurement), which `jsonschema-rs` removes; the parallel pool takes the rest from about 6 min of compute to 52 s of wall time on 10 cores. The variants, 78 jobs over the pool, likewise.
