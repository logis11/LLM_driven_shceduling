# daemon/

The recognition daemon: visible projection → telemetry → recognizer → validator → config mapper, emitting config schedules and recognition logs (`docs/daemon/daemon-guide.md`). Tree owner: 박이안.

One artifact in this tree is not the daemon builder's: **`driver-table/`** — the driver table (`docs/data-contracts.md`, the driver-table section) is 인지오's to author and freeze. It lives here because the daemon's config mapper is its reader.

```
driver-table/
  schema/driver-table.schema.json   # the table's shape (frozen with the contract)
  prior.yaml                        # the prior table  — written from theory (Phase 6)
  calibrated.yaml                   # the calibrated table — tuned on the throwaway pool (later)
tools/
  drivertable/config_schema.py      # importable copy of the frozen cpu_scheduler config schema + vocabulary
  drivertable/lint.py               # table lint: schema + the cross-checks JSON Schema cannot express
  lint.py                           # CLI: make lint
  tests/                            # make test
```

`config_schema.py` is the first machine-readable form of `docs/recognition-vocabulary.md` §1–§2; the daemon's validator should import it rather than re-typing the field lists, so the lint and the validator can never disagree.

```
pip install -r tools/requirements.txt
make lint      # exit 1 on any violation; "nothing to lint" until the tables land
make test
```
