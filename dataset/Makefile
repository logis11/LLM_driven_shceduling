PY ?= python3

dataset:            ## derive variants + grid, compile timelines -> build/ + manifest
	$(PY) tools/derive.py
	$(PY) tools/compile.py

variants:           ## the RQ0 gate spec's sensitivity variants -> build/ + variants manifest (needs `dataset`)
	$(PY) tools/variants.py

generated:          ## the generated layer: the sets grids.yaml names, composed or renamed from the C1 task sets -> generated/ (not committed) + build/ + one manifest per set
	$(PY) tools/generate.py

lint:               ## the checks before a compile: repo + timeline lints (no writes; the canonical lints run inside the compile)
	$(PY) tools/lint.py

test:               ## invariant test suite
	$(PY) -m pytest tools/tests -q

check:              ## CI gate, after `dataset variants generated`: derived files, grid (all 32 cells), every manifest equal to its committed bytes, build/ equal to their union
	$(PY) tools/derive.py --check --require-coverage
	$(PY) tools/check_build.py

.PHONY: dataset variants generated lint test check
