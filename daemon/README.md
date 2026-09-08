# daemon/

The recognition daemon: visible projection → telemetry → recognizer → validator → config mapper, emitting config schedules and recognition logs (`docs/daemon/daemon-guide.md`). Tree owner: 박이안.

One artifact in this tree is not the daemon builder's: **`driver-table/`** — the driver table (`docs/data-contracts.md`, the driver-table section) is 인지오's to author and freeze. It lives here because the daemon's config mapper is its reader.

```
driver-table/
  schema/driver-table.schema.json   # the table's shape (frozen with the contract)
  prior.yaml                        # the prior table  — written from theory (Phase 6)
  calibrated.yaml                   # the calibrated table — tuned on the throwaway pool (later)
tools/
  daemon/projection.py              # the parse boundary: workload file -> visible projection
  daemon/groundtruth.py             # the answer key — oracle-only, isolation enforced by a test
  daemon/corpus.py                  # the compiled workload corpus, checked against the build manifest
  daemon/jsonio.py                  # canonical JSON: the byte-identical-rerun guarantee
  daemon/errors.py                  # the input-boundary refusals
  drivertable/config_schema.py      # importable copy of the frozen cpu_scheduler config schema + vocabulary
  drivertable/lint.py               # table lint: schema + the cross-checks JSON Schema cannot express
  project.py                        # CLI: make corpus, and printing a projection by hand
  lint.py                           # CLI: make lint
  tests/                            # make test
```

## Inputs

The daemon reads the dataset tree's build output, which is not committed —
`dataset/build.manifest.json` carries a sha256 per artifact instead. Build it
once, then check it:

```
make -C dataset dataset     # writes dataset/build/coreset-{single,native}/
make -C daemon corpus       # every file matches the manifest, 24 of them
```

Experiments run on `coreset-single` (workload/building-plan §2); `coreset-native`
is built but unread. Tests that need real workloads skip when the build is
absent, so a fresh clone is green without it — CI builds it first.

## The information rule, in code

`docs/daemon/daemon-guide.md` §2.1: a recognizer may see process names, counts
and pinned lifetime times, and nothing else. That is why `projection.py` drops
task programs, ids, `wake` events and `ground_truth` at the parse boundary and
returns frozen dataclasses — there is no attribute to follow back to the file —
and why the answer key lives in its own module that only the oracle may import.
`tests/test_isolation.py` reads the package with `ast` and fails the build if
anything outside the allowlist starts importing it. Print a projection to check
it by eye against the timeline:

```
python3 tools/project.py c1-compile
python3 tools/project.py --summary
```

`config_schema.py` is the first machine-readable form of `docs/recognition-vocabulary.md` §1–§2; the daemon's validator should import it rather than re-typing the field lists, so the lint and the validator can never disagree.

```
pip install -r tools/requirements.txt
make corpus    # dataset/build/ matches dataset/build.manifest.json
make lint      # exit 1 on any violation; "nothing to lint" until the tables land
make test
```

The daemon package itself is standard library only, deliberately: its outputs
must be byte-identical across reruns and machines, and every dependency is a
way for that to stop being true.
