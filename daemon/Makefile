PY ?= python3

corpus:             ## verify dataset/build against dataset/build.manifest.json
	$(PY) tools/project.py --verify

lint:               ## driver-table lint (schema + cross-checks) over driver-table/*.yaml
	$(PY) tools/lint.py

test:               ## daemon + driver-table tooling tests
	$(PY) -m pytest tools/tests -q

.PHONY: corpus lint test
