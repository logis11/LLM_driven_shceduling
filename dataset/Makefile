PY ?= python3

dataset:            ## derive variants + grid, compile timelines -> build/ + manifest
	$(PY) tools/derive.py
	$(PY) tools/compile.py

variants:           ## the RQ0 gate spec's sensitivity variants -> build/ + variants manifest (needs `dataset`)
	$(PY) tools/variants.py

lint:               ## the checks before a compile: repo + timeline lints (no writes; the canonical lints run inside the compile)
	$(PY) tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest tools/tests -q

check:              ## CI gate, after `dataset variants`: derived files, grid (all 32 cells), both manifests equal to their committed bytes, build/ equal to them
	$(PY) tools/derive.py --check --require-coverage
	$(PY) tools/check_build.py

.PHONY: dataset variants lint test check
