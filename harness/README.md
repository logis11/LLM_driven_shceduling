# harness/

The experiment harness. This tree is 인지오's. Definitions the code implements: `docs/harness/metrics.md`; input formats: `docs/data-contracts.md` (§9 trace, §4 run-file view, §8 recognition log).

- `tools/harness/` — the Python package: `reader.py` (trace + run-file readers), `primitives.py` (raw observations from one pair), `records.py` (identity, row order, CSV, schema validation). `tools/records.py` is the CLI: one pair → one records CSV, guard messages on stderr.
- `records/schema/records.schema.json` — the machine schema for one records row (metrics doc §5).
- `tools/tests/` — tests; `fixtures/` holds the four hand-written mock pairs with their expected records (`fixtures/README.md`).
- `make lint` parses every fixture pair under the frozen contracts and validates its expected records against the schema; `make test` runs the suite. CI: `.github/workflows/harness.yml`. Dependencies: `tools/requirements.txt`.
