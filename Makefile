PY ?= python3

dataset:            ## compile timelines -> dataset/build/ + manifest
	$(PY) dataset/tools/compile.py

lint:               ## repo + timeline + canonical lints (no writes)
	$(PY) dataset/tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest dataset/tools/tests -q

check:              ## CI gate: recompile and verify the committed manifest
	$(PY) dataset/tools/compile.py --check

.PHONY: dataset lint test check
