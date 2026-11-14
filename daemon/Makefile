PY ?= python3
# The string the runner's machine configuration names as the daemon's `version`
# (harness/runner.example.yaml): the git blob hash of the source bytes the daemon runs — daemon.py
# and the drivertable module it imports — so it changes exactly when they do (the integration
# gate's spec, decision 10, _dev/docs/spec/jioh/task-10.2-integration-gate.md)
SOURCES := daemon.py tools/drivertable/__init__.py tools/drivertable/config_schema.py
VERSION := daemon@$(shell cat $(SOURCES) | git hash-object --stdin | cut -c1-12)

lint:              ## driver-table lint (schema + cross-checks) over driver-table/*.yaml
	$(PY) tools/lint.py

test:               ## driver-table tooling tests
	$(PY) -m pytest tools/tests -q

version:            ## the daemon's version string, daemon@<12 hex>
	@echo $(VERSION)

.PHONY: lint test version
