# harness/

The experiment harness. This tree is 인지오's. Definitions the code implements: `docs/harness/metrics.md`; input formats: `docs/data-contracts.md` (§9 trace, §4 run-file view, §7 config schedule, §8 recognition log).

- `tools/harness/` — the Python package: `reader.py` (trace, run-file, and config-schedule readers), `primitives.py` (raw observations from one pair, plus the schedule for `switch_window`), `records.py` (identity, row order, CSV, schema validation). `tools/records.py` is the CLI: one pair → one records CSV, `--schedule` for the config schedule, guard messages on stderr.
- `tools/check_mlfq_levels.py` — beside the harness, not part of it: reads the `x_mlfq_level` lines the reader skips and checks that each switch window covers its hogs' last demotion (metrics doc §12). Exit 1 on a miss, 2 when a switch into MLFQ has no schedule to size it.
- `records/schema/records.schema.json` — the machine schema for one records row (metrics doc §5).
- `scoring/scoring-spec.yaml` — the scoring spec (Phase 6): per coreset file, the terms whose normalised shares the file's score sums; `scoring/schema/scoring-spec.schema.json` its schema; `tools/harness/scoring.py` the loader and lint (entity exists in the compiled workload, scored metric/aggregate pairs and directions, positive weights, windows inside the file, derived files verbatim from their base per the dataset's recipes, and a variant without a declared base must differ from it); `tools/scoring_lint.py` the CLI.
- `tools/tests/` — tests; `fixtures/` holds the five hand-written mock pairs with their expected records (`fixtures/README.md`).
- `make lint` parses every fixture pair under the frozen contracts, validates its expected records against the schema, and lints the scoring spec against the compiled coreset under `dataset/build/coreset-single` (build it first: `make -C dataset dataset`); `make test` runs the suite. CI: `.github/workflows/harness.yml`. Dependencies: `tools/requirements.txt`.
