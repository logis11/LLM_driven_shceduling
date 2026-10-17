PY ?= python3

lint:               ## fixture pairs under the frozen contracts; the scoring spec against schema, coreset, recipes; the guard spec against schema, registry, recipes; every experiment spec against schema, coreset, pins
	$(PY) tools/lint.py
	$(PY) tools/scoring_lint.py
	$(PY) tools/guards_lint.py
	$(PY) tools/experiment_lint.py

test:               ## the suite without the two coreset-wide mock tests (what CI runs; they exceed a 16 GB runner)
	$(PY) -m pytest tools/tests -q -m "not coreset_wide"

test-full:          ## the whole suite, the coreset-wide tests included (about 10 GB resident; run at home)
	$(PY) -m pytest tools/tests -q

smoke:              ## the full pipeline on the mocks over every scored coreset file (8.6): a generated throwaway spec, runs under runs/
	$(PY) tools/smoke.py --machine runner.example.yaml

.PHONY: lint test test-full smoke
