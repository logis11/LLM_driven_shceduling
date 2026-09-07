PY ?= python3

lint:               ## driver-table lint (schema + cross-checks) over driver-table/*.yaml
	$(PY) tools/lint.py

test:               ## driver-table tooling tests
	$(PY) -m pytest tools/tests -q

.PHONY: lint test
