PY ?= python3

lint:               ## fixture pairs under the frozen contracts; the scoring spec against schema, coreset, recipes
	$(PY) tools/lint.py
	$(PY) tools/scoring_lint.py

test:               ## reader / primitives / records tests
	$(PY) -m pytest tools/tests -q

.PHONY: lint test
