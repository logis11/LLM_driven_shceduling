PY ?= python3

dataset:            ## derive variants + grid, compile timelines -> build/ + manifest
	$(PY) tools/derive.py
	$(PY) tools/compile.py

variants:           ## the RQ0 gate spec's sensitivity variants -> build/ + variants manifest (needs `dataset`)
	$(PY) tools/variants.py

lint:               ## repo + timeline + canonical lints (no writes)
	$(PY) tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest tools/tests -q

check:              ## CI gate: derived files, grid (all 32 cells), both manifests, and build/ equal to them (needs `dataset variants`)
	$(PY) tools/derive.py --check --require-coverage
	$(PY) tools/compile.py --check
	$(PY) tools/variants.py --check
	$(PY) tools/check_build.py

.PHONY: dataset variants lint test check
