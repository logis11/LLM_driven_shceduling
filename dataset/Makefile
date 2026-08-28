PY ?= python3

dataset:            ## derive variants + grid, compile timelines -> build/ + manifest
	$(PY) tools/derive.py
	$(PY) tools/compile.py

lint:               ## repo + timeline + canonical lints (no writes)
	$(PY) tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest tools/tests -q

check:              ## CI gate: verify derived files, grid, and manifest
	$(PY) tools/derive.py --check
	$(PY) tools/compile.py --check

.PHONY: dataset lint test check
