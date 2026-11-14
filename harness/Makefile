PY ?= python3

lint:               ## fixture pairs under the frozen contracts; the scoring spec against schema, coreset, recipes; the guard spec against schema, registry, recipes; every experiment spec against schema, coreset, pins
	$(PY) tools/lint.py
	$(PY) tools/scoring_lint.py
	$(PY) tools/guards_lint.py
	$(PY) tools/experiment_lint.py

test-quick:         ## the suite without the tests marked slow (over about two seconds each): the edit loop
	$(PY) -m pytest tools/tests -q -m "not slow and not coreset_wide"

test:               ## the suite without the two coreset-wide mock tests (what CI runs; they exceed a 16 GB runner)
	$(PY) -m pytest tools/tests -q -m "not coreset_wide"

test-full:          ## the whole suite, the coreset-wide tests included (about 10 GB resident; run at home)
	$(PY) -m pytest tools/tests -q

smoke:              ## the full pipeline on the mocks over every scored coreset file (8.6): a generated throwaway spec, runs under runs/
	$(PY) tools/smoke.py --machine runner.example.yaml

gate:               ## the integration gate (10.2) on runner.yaml's real programs: unit tests and mutants, fixture replay, daemon comparison, short run
	$(PY) tools/integration_gate.py --machine runner.yaml

gate-status:        ## the integration gate's parts against the RQ0 gate spec's version pins
	$(PY) tools/integration_gate.py --status --machine runner.yaml

.PHONY: lint test-quick test test-full smoke gate gate-status
