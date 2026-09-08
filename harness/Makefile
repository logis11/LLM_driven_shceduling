PY ?= python3

lint:               ## every fixture pair (run file + trace) parses under the frozen contracts
	$(PY) tools/lint.py

test:               ## reader / primitives / records tests
	$(PY) -m pytest tools/tests -q

.PHONY: lint test
