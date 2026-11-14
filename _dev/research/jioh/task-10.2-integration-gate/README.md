# The integration gate's results (10.2)

Each part of the gate (`harness/tools/integration_gate.py`; `make -C harness gate`) writes `<part>.json` — passed or not, when, the version strings it checked, its figures — and `<part>.log`, its full output. `make -C harness gate-status` reads them against the RQ0 gate spec's `pins.simulator` and `pins.daemon`.

| part | what it ran | on |
|---|---|---|
| `unit` | the seven unit tests of `simulator/tests/` on the binary, then the five mutants of `simulator/tests/mutants.py`, each test failing on its mutant | `simulator@0d323c84470a`, Apple clang 21.0.0, the binary's SHA-256 in `unit.json` |
| `replay` | the nine fixtures with a trace under `harness/tools/tests/fixtures/`, each replayed twice through the binary with the invocation contract's flags; lines per µs and records against the fixture | `simulator@0d323c84470a` |
| `daemon` | `daemon/daemon.py` and the harness's mock daemon on the 19 425 runs the runner expands from `harness/experiments/rq0-gate.yaml`, schedule and log compared byte for byte | `daemon@62c71f0d2de0` |
| `short` | `harness/tools/smoke.py` on the home machine's configuration over seven files (`c1-photo`, `c1-office`, `c7-mail`, `c2-p2b`, `c1-gaming`, `c7-compile`, `c1-compile`), runs under `runs/integration-gate/` | both |

The paths in the files are relative to the repository root.
