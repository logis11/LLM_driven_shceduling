PY ?= python3

dataset:            ## derive variants + grid, compile timelines -> build/ + manifest
	$(PY) dataset/tools/derive.py
	$(PY) dataset/tools/compile.py

lint:               ## repo + timeline + canonical lints (no writes)
	$(PY) dataset/tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest dataset/tools/tests -q

check:              ## CI gate: verify derived files, grid, and manifest
	$(PY) dataset/tools/derive.py --check
	$(PY) dataset/tools/compile.py --check

.PHONY: dataset lint test check
