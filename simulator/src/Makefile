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
# §7 item 6) and demand across config switches (memo_261010 D2)
check: sim
	python3 ../tests/test_batch_class.py ./sim
	python3 ../tests/test_switch_demand.py ./sim

.PHONY: version check
