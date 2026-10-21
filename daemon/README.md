# daemon/

The recognition daemon: visible projection → telemetry → recognizer → validator → config mapper, emitting config schedules and recognition logs (`docs/daemon/daemon-guide.md`). Tree owner: 박이안.

One artifact in this tree is not the daemon builder's: **`driver-table/`** — the driver table (`docs/data-contracts.md`, the driver-table section) is 인지오's to author and freeze. It lives here because the daemon's config mapper is its reader.

```
driver-table/
  prior.yaml                        # the prior table (Phase 6): 32 rows from theory, every judgement with its references.md ids
  schema/driver-table.schema.json   # the table's shape (frozen with the contract)
  prior.yaml                        # the prior table  — written from theory (Phase 6)
  calibrated.yaml                   # the calibrated table — tuned on the driver table tuning set (later)
tools/
  drivertable/config_schema.py      # importable copy of the frozen cpu_scheduler config schema + vocabulary
  drivertable/lint.py               # table lint: schema + the cross-checks JSON Schema cannot express
  lint.py                           # CLI: make lint
  tests/                            # make test
```

`config_schema.py` is the first machine-readable form of `docs/recognition-vocabulary.md` §1–§2; the daemon's validator should import it rather than re-typing the field lists, so the lint and the validator can never disagree.

```
pip install -r tools/requirements.txt
make lint      # exit 1 on any violation; also resolves every `sources` id against docs/references.md
make test      # the driver-table tooling tests and the daemon's contract tests
```

## `daemon.py` — the running skeleton

`daemon.py` is the daemon itself, as much of it as runs today. It is the pipeline the
guide draws — visible projection → telemetry snapshots → recognizer → validator → config
mapper — with the three conditions the RQ0 run needs that take no model:

| condition | what it does |
|---|---|
| `fixed` | the control: the boot default alone, one schedule entry, no query points |
| `oracle` | reads the answer key; the segment covering a query point gives the mode and the attribute |
| `random` | a seeded uniform draw over the table's rows — the floor a recognizer must beat |

```sh
python3 daemon.py --workload   /abs/…/c2-p1a.workload.json \
                  --condition  oracle --telemetry focus \
                  --driver-table /abs/daemon/driver-table/prior.yaml \
                  --boot-default /abs/harness/boot-defaults/ostep.json \
                  --out-schedule /abs/…/schedule.json \
                  --out-log      /abs/…/log.json
```

Every flag is required, `--seed` exactly for a drawing condition, nothing goes to standard
output, and exit 0 means both files were written (`docs/data-contracts.md` §11). The five
conditions that need a recognizer — `shipped_catalogue`, `strongest_name_table`,
`llm_vocab`, `llm_algo`, `llm_full` — exit non-zero saying so. Each is one function away:
the seat is `RECOGNIZERS`, a map from condition name to a function from one telemetry
snapshot to a proposal.

**Not here**: no LLM client, no record/replay store, no hold time or hysteresis, and no
clamping path — the three conditions above compose their configurations from the driver
table, so they are valid by construction and only `unmodified` and `fallback` are ever
emitted. The validator seat exists and they pass through it; a `clamped` or `held` entry
needs a recognizer that can produce one.

**Verified** (2026-10-20): byte-identical to the harness's reference mock
(`harness/tools/tests/mocks/daemon.py`, faithful for these three conditions by the Phase 8
spec) over 25 workloads × 3 conditions × 2 telemetry shapes, 150/150 — schedules and logs
both. End to end into the simulator: `fixed` and `oracle` schedules on `c2-p1a`,
`c1-gaming` and `c2-p2b` run through `simulator/src/sim`, every entry reaching a
`config_applied` line. `tools/tests/test_daemon.py` pins the contract invariants: the
telemetry rules that place the query points, one schedule entry per query point, the log's
`validation` sequence equal to the schedule's `provenance`, the canonical key order of a
composed configuration, the refusals, and byte-identical reruns from one argument line.
