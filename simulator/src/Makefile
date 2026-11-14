# The reference simulator. `make` builds ./sim; `make version` prints the string the trace header
# carries in `sim`, which the runner's machine configuration names as the simulator's `version`
# (harness/runner.example.yaml). The version is the git blob hash of the source bytes, so it
# changes exactly when the source does — a stale binary names a stale version.
CXX      ?= g++
CXXFLAGS ?= -std=c++17 -O2 -g -Wall -Wextra
VERSION  := simulator@$(shell cat sim.cpp mini_json.hpp | git hash-object --stdin | cut -c1-12)

sim: sim.cpp mini_json.hpp
	$(CXX) $(CXXFLAGS) -DSIM_VERSION='"$(VERSION)"' -o $@ sim.cpp

version:
	@echo $(VERSION)

# the unit tests on this binary (black-box, a few seconds): the batch-class rule's two (batch memo
# §7 item 6) and demand across config switches (memo_261010 D2); then the RQ0 gate spec's
# conformance items no hand fixture shows (`simulator-conformance`; the integration gate's spec,
# _dev/docs/spec/jioh/task-10.2-integration-gate.md, decisions 4, 6 and 7): the cap's ceiling (d),
# the strict idle class (e), the frame chain in EDF's deadline class (f), the spawn-table wake and
# the children wait on the two reference workloads (i, g), the invocation contract's refusals (h)
check: sim
	python3 ../tests/test_batch_class.py ./sim
	python3 ../tests/test_switch_demand.py ./sim
	python3 ../tests/test_cap_ceiling.py ./sim
	python3 ../tests/test_idle_class.py ./sim
	python3 ../tests/test_edf_chain.py ./sim
	python3 ../tests/test_spawn_children.py ./sim
	python3 ../tests/test_invocation.py ./sim

# each behavioural test above fails on a simulator without its behaviour: a mutant of this source
# with the behaviour's line taken out (the integration gate's spec, decision 8)
mutants:
	python3 ../tests/mutants.py

.PHONY: version check mutants
