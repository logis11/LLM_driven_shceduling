# harness/

The experiment harness. This tree is 인지오's. Definitions the code implements: `docs/harness/metrics.md`; input formats: `docs/data-contracts.md` (§9 trace, §4 run-file view, §8 recognition log).

- `tools/harness/` — the Python package: `reader.py` (trace + run-file readers), primitives and the records writer as they land.
- `tools/tests/` — tests; `fixtures/` holds the four hand-written mock pairs with their expected records (`fixtures/README.md`).
- `make lint` parses every fixture pair under the frozen contracts; `make test` runs the suite. Dependencies: `tools/requirements.txt`.
