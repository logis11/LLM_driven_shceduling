#!/usr/bin/env bash
# machine_gate.sh — same-machine repeats (9.6 changelog D10). Source it.
# GitHub-hosted runners guarantee a shape (4 vCPU, 16 GB), not a processor: the jobs of one batch are independent
# draws from a pool of several CPU models, and one core of one model can be a quarter faster than one core of
# another (9.6 campaign: Xeon Platinum 8573C against EPYC 7763, cc1 CPU per process 0.74). A measured value is
# "this software on this machine" (9.5 D10), so a campaign names its machine and a job that drew another model
# stops before measuring anything.
#
#   machine_gate "<substring of the wanted `model name`>"   # empty = no gate
# returns 0 when the gate is open (or unset), 1 when this runner is another model. The caller records and exits.
machine_model() { sed -n 's/^model name[[:space:]]*:[[:space:]]*//p' /proc/cpuinfo 2>/dev/null | head -1; }
machine_gate() {
  local want="${1:-}" have; have="$(machine_model)"
  [ -z "$want" ] && return 0
  case "$have" in *"$want"*) return 0;; *) return 1;; esac
}
