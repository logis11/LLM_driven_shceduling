PY ?= python3

lint:               ## fixture pairs under the frozen contracts; the scoring spec against schema, coreset, recipes; the guard spec against schema, registry, recipes; every experiment spec against schema, coreset, pins
	$(PY) tools/lint.py
	$(PY) tools/scoring_lint.py
	$(PY) tools/guards_lint.py
	$(PY) tools/experiment_lint.py

test:               ## reader / primitives / records tests
	$(PY) -m pytest tools/tests -q

.PHONY: lint test
