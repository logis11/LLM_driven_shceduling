#!/usr/bin/env python3
"""Write the batch-loop tables of the compile and background entries from their pooled records.

batch_fold_in.py [--check]

`cpu-batch` (9.6; its `python3` program from 9.10's MNIST campaign), `compiler-child` and `build-orchestrator` (9.6), `file-backup`, `file-archiver` and `game-download`
(9.7), `package-upgrade` (9.10), `module-build-orchestrator` and `module-compiler-child` (9.10), and `file-indexer` (9.10) carry the quantile tables, each one pooled table of the campaign's record: a program's runs between voluntary
blocks and the block after each run (9.6 D21, D22, D25; 9.7 D29), the object job's per-(role, step) CPU (9.6 D19,
D20), make's dispatch run. Each is written in the library's table form (distribution.yaml_table: the ten quantiles,
the extremes, the interval means), keeping the param's own sampling and source tag; nothing else in the entries is
touched. --check exits 1 if dataset/archetypes.yaml differs from what the records give.
"""

import json
import os
import re
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.distribution import yaml_table  # noqa: E402
from meas.background import modbuild  # noqa: E402

RESEARCH = os.path.join("_dev", "research", "jioh")
POOLS = {"build": os.path.join(RESEARCH, "task-9.6-compile", "campaign", "results", "pooled.json"),
         "borg": os.path.join(RESEARCH, "task-9.7-background-io", "campaign", "results", "borg-pooled.json"),
         "7z": os.path.join(RESEARCH, "task-9.7-background-io", "campaign", "results", "7z-pooled.json"),
         "steamcmd": os.path.join(RESEARCH, "task-9.7-background-io", "campaign", "results", "steamcmd-pooled.json"),
         "upgrade": os.path.join(RESEARCH, "task-9.10-scenarios-timelines", "campaign", "upgrade", "results", "pooled.json"),
         "dkms": os.path.join(RESEARCH, "task-9.10-scenarios-timelines", "campaign", "dkms", "results", "pooled.json"),
         "tracker": os.path.join(RESEARCH, "task-9.10-scenarios-timelines", "campaign", "tracker", "results", "pooled.json"),
         "mnist": os.path.join(RESEARCH, "task-9.10-scenarios-timelines", "campaign", "mnist", "results", "pooled.json")}

# (archetype, param) -> (record, path to the pooled table)
_PROGRAMS = {"clamscan": "clamscan", "ffmpeg": "ffmpeg", "handbrakecli": "handbrake"}   # tracker: file-indexer (9.10 D70)
TABLES = {}
for _p, _phase in _PROGRAMS.items():
    TABLES[("cpu-batch", f"{_p}_run")] = ("build", ("phases", _phase, "shape", "runs_between_blocks_us"))
    TABLES[("cpu-batch", f"{_p}_block")] = ("build", ("phases", _phase, "shape", "blocks_after_runs_us"))
for _role, _steps in (("sh", 4), ("gcc", 3), ("cc1", 1), ("as", 1), ("fixdep", 1), ("rm", 1)):
    for _n in range(1, _steps + 1):
        TABLES[("compiler-child", f"{_role}_step_{_n}")] = (
            "build", ("phases", "build-j8-warm", "object_members", "step_cpu_us", f"{_role} {_n}/{_steps}"))
# 9.10 D85: `python3` re-measured as PyTorch's basic MNIST example, from the MNIST campaign's record
TABLES[("cpu-batch", "python3_run")] = ("mnist", ("runs", "mnist", "phases", "mnist-train", "all", "batch_run_us"))
TABLES[("cpu-batch", "python3_block")] = ("mnist", ("runs", "mnist", "phases", "mnist-train", "all", "batch_block_us"))
TABLES[("build-orchestrator", "dispatch_overhead")] = ("build", ("phases", "build-j8-warm", "dispatch", "per_dispatch_us"))
for _aid, _app, _phase in (("file-backup", "borg", "borg-first-warm"), ("file-archiver", "7z", "7z-mmt8-warm"),
                           ("game-download", "steamcmd", "steam-fresh-shaped"), ("package-upgrade", "upgrade", "upgrade-install"),
                           ("file-indexer", "tracker", "tracker-index")):
    TABLES[(_aid, f"{_app}_run")] = (_app, ("runs", _app, "phases", _phase, "all", "batch_run_us"))
    TABLES[(_aid, f"{_app}_block")] = (_app, ("runs", _app, "phases", _phase, "all", "batch_block_us"))

# 9.10 D52–D54: the module build's per-(kind, member, step) CPU, make's dispatch run and the serial tail's batch loop
_MB = ("runs", "dkms", "phases", "dkms-install", "module_build")
for _kind, _tree in modbuild.TREES.items():
    for _mid, _role, _n in modbuild.members(_tree):
        for _i in range(1, _n + 1):
            TABLES[("module-compiler-child", f"{_kind.replace('-', '_')}_{_mid}_step_{_i}")] = (
                "dkms", _MB + ("steps", f"{_kind} {_mid} {_i}/{_n}"))
TABLES[("module-build-orchestrator", "dispatch_overhead")] = ("dkms", _MB + ("dispatch_us",))
TABLES[("module-build-orchestrator", "tail_run")] = ("dkms", _MB + ("tail_run_us",))
TABLES[("module-build-orchestrator", "tail_block")] = ("dkms", _MB + ("tail_block_us",))

PARAM_LINE = re.compile(r'^(\s*)\{dist: quantiles, .*sampling: (\S+), source: "([^"]+)"\}\s*$')


def load_pools(repo_root):
    return {name: json.load(open(os.path.join(str(repo_root), path))) for name, path in POOLS.items()}


def rewrite(text, pools):
    lines = text.split("\n")
    archetype, written = None, set()
    for i, line in enumerate(lines):
        m = re.match(r"^  ([a-z0-9-]+):\s*$", line)
        if m:
            archetype = m.group(1)
            continue
        m = re.match(r"^\s+([a-z0-9_]+):\s*$", line)
        if not m or (archetype, m.group(1)) not in TABLES:
            continue
        record, path = TABLES[(archetype, m.group(1))]
        node = pools[record]
        for key in path:
            node = node[key]
        pm = PARAM_LINE.match(lines[i + 1])
        if not pm:
            raise SystemExit(f"{archetype}.{m.group(1)}: the line after the param is not a one-line quantiles table")
        lines[i + 1] = pm.group(1) + yaml_table(node["table"], pm.group(3), scale=1.0, sampling=pm.group(2))
        written.add((archetype, m.group(1)))
    missing = sorted(set(TABLES) - written)
    if missing:   # a table the library no longer holds is a failure, not a table skipped
        raise SystemExit(f"not in the library: {', '.join(f'{a}.{p}' for a, p in missing)}")
    return "\n".join(lines)


def main():
    repo = os.path.dirname(os.path.dirname(TOOLS))
    path = os.path.join(repo, "dataset", "archetypes.yaml")
    text = open(path).read()
    new = rewrite(text, load_pools(repo))
    if "--check" in sys.argv[1:]:
        sys.exit(0 if new == text else 1)
    open(path, "w").write(new)
    print(f"{path}: {len(TABLES)} batch tables written")


if __name__ == "__main__":
    main()
