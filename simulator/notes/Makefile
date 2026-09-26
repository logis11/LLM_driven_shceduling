CXX      ?= g++
CXXFLAGS ?= -std=c++17 -O0 -g -Wall -Wextra -fsanitize=address,undefined
STAGES   := a b c d e f g h i j k l m n o p
BIG      := q r          # 실제 coreset 파일을 돌리므로 -O2, sanitizer 없이

all: $(addprefix sim_,$(STAGES)) $(addprefix sim_,$(BIG))

sim_%: sim_%.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

sim_q: sim_q.cpp mini_json.hpp
	$(CXX) -std=c++17 -O2 -g -Wall -Wextra -o $@ $<
sim_r: sim_r.cpp mini_json.hpp
	$(CXX) -std=c++17 -O2 -g -Wall -Wextra -o $@ $<

lines:
	@for f in sim_*.cpp; do printf "%-12s %4s\n" $$f $$(grep -vcE '^[[:space:]]*(//|$$)' $$f); done

clean:
	rm -f $(addprefix sim_,$(STAGES)) $(addprefix sim_,$(BIG))

.PHONY: all lines clean
