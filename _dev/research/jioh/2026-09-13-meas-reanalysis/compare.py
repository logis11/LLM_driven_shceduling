#!/usr/bin/env python3
"""Corrected summary vs dataset/meas/summary.json, plus the task-9.3 done check.

Usage: compare.py  (run from anywhere; writes comparison.md next to itself)

Done check (task-9.3 spec decision 6):
  1. every field no fix touches is byte-identical to the current summary;
  2. every fixed number agrees with the 2026-09-13 audit's independent
     computation where one exists (files under ../2026-09-13-verification/).
"""

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
AUDIT = HERE.parent / "2026-09-13-verification"

# Which fix may change a field. Anything else must be byte-identical.
FIXES = [
    ("#1 compiler child = cc1", re.compile(
        r"compiler(_cold)?_(lifetime|children|cpu_mean_us|life_mean_us|"
        r"peak_concurrent|family_exits|family_peak_concurrent)")),
    ("#12 make's own children", re.compile(
        r"/(make_dispatch_us|fork_rate_hz|make_children)")),
    ("#5 renderer set", re.compile(r"/(chromium_wakes|across_repeats/chromium/)")),
    ("#3 wake counter", re.compile(r"/across_repeats/wake_counter$")),
]
ZERO_KEYS = ("p90_us", "n_nonpositive", "median_all_us")  # #9


def flat(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from flat(value, f"{path}/{key}")
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from flat(value, f"{path}[{i}]")
    else:
        yield path, node


def fix_for(path, new_flat):
    for label, pattern in FIXES:
        if pattern.search(path):
            return label
    parent, _, key = path.rpartition("/")
    if key in ZERO_KEYS and f"{parent}/n_nonpositive" in new_flat:
        return "#9 zeros reported"
    return None


def audit_compiler():
    """{(repeat, prefix): figures} from cc1_cpu.txt and method_checks_cli3.txt."""
    out = {}
    prefix_of = {"kernel-build-j8": "compiler", "kernel-build-cold": "compiler_cold"}
    key = None
    for line in (AUDIT / "meas/method_checks_cli3.txt").open():
        m = re.match(r"(meas-cli-r\d) (kernel-build-\S+) total (\d+)", line)
        if m:
            key = (m.group(1), prefix_of[m.group(2)])
            out.setdefault(key, {})["family_exits"] = int(m.group(3))
            continue
        m = re.match(r"\s+cc1\s+n=\s*(\d+) median_us=\s*(\d+) sl=([\d.]+)", line)
        if m and key:
            out[key].update(children=int(m.group(1)), lifetime_median_us=int(m.group(2)),
                            lifetime_sigma_log=float(m.group(3)))
    for line in (AUDIT / "meas/cc1_cpu.txt").open():
        m = re.match(r"(meas-cli-r\d) (kernel-build-\S+) .* peak cc1 live (\d+)", line)
        if m:
            key = (m.group(1), prefix_of[m.group(2)])
            out[key]["peak_concurrent"] = int(m.group(3))
            continue
        m = re.match(r"\s+cc1: cpu s [\d.]+ exits (\d+) mean cpu/cc1 exit us (\d+)", line)
        if m and key:
            out[key]["cpu_mean_us"] = int(m.group(2))
    return out


def audit_renderers():
    """{repeat: [gap ms]} for processes the audit typed as renderer exactly
    (its label has no '?': the pid itself logged --type=renderer)."""
    out = {}
    for line in (HERE / "audit-chrome-types.txt").open():
        m = re.match(r"(meas-gui-r\d) chromium-10-tabs (\[.*\])", line)
        if m:
            labels = json.loads(m.group(2).replace("'", '"'))
            out[m.group(1)] = sorted(
                int(label.rsplit(":", 1)[1][:-2]) for label in labels
                if label.startswith("renderer") and "?" not in label.rsplit(":", 1)[0])
    return out


def main():
    old = json.load((REPO / "dataset/meas/summary.json").open())
    new = json.load((HERE / "summary.json").open())
    old_flat, new_flat = dict(flat(old)), dict(flat(new))
    failures, changed, added, removed = [], [], [], []

    for path, value in old_flat.items():
        fix = fix_for(path, new_flat)
        if path not in new_flat:
            (removed if fix else failures).append((path, fix, value, None))
        elif json.dumps(value) != json.dumps(new_flat[path]):
            (changed if fix else failures).append((path, fix, value, new_flat[path]))
    for path, value in new_flat.items():
        if path not in old_flat:
            fix = fix_for(path, new_flat)
            (added if fix else failures).append((path, fix, None, value))
    untouched = sum(1 for p in old_flat if not fix_for(p, new_flat))

    checks = []
    for (repeat, prefix), figures in sorted(audit_compiler().items()):
        got = new["cli_repeats"][repeat]
        mine = {"children": got[f"{prefix}_children"],
                "family_exits": got[f"{prefix}_family_exits"],
                "lifetime_median_us": got[f"{prefix}_lifetime"]["median_us"],
                "lifetime_sigma_log": got[f"{prefix}_lifetime"]["sigma_log"],
                "cpu_mean_us": got[f"{prefix}_cpu_mean_us"],
                "peak_concurrent": got[f"{prefix}_peak_concurrent"]}
        for name, expected in figures.items():
            checks.append((f"{repeat} {prefix}_{name}", mine[name], expected,
                           "cc1_cpu.txt / method_checks_cli3.txt"))
        checks.append((f"{repeat} {prefix}_family_peak_concurrent",
                       got[f"{prefix}_family_peak_concurrent"], 16,
                       "meas-report.md §2.3 (16 in every repeat)"))
    daemons = new["across_repeats"]["daemons"]["work"]
    for name, expected in (("n", 29), ("n_nonpositive", 22), ("median_all_us", 62)):
        checks.append((f"daemons.work.{name}", daemons[name], expected,
                       "meas-report.md X9 (29 of 51; plain median 62 µs)"))
    for repeat, gaps in sorted(audit_renderers().items()):
        mine = sorted(round(w["gap_us"] / 1000) for w in new["gui_repeats"][repeat]["chromium_wakes"])
        checks.append((f"{repeat} renderer gaps (ms)", mine, gaps, "audit-chrome-types.txt"))
    check_failures = [c for c in checks if c[1] != c[2]]

    lines = ["# Corrected meas-ci summary vs `dataset/meas/summary.json`", "",
             "Generated by `compare.py`.", "",
             "## Done check", "",
             f"- Untouched fields: {untouched} of {len(old_flat)}; "
             f"{'all byte-identical' if not failures else f'{len(failures)} differ'}.",
             f"- Audit agreement: {len(checks) - len(check_failures)} of {len(checks)} figures agree.", ""]
    for path, fix, before, after in failures:
        lines.append(f"  - UNEXPECTED `{path}`: {before!r} → {after!r}")
    lines += ["| Figure | Corrected summary | Audit | Audit source |", "|---|---|---|---|"]
    for name, mine, expected, source in checks:
        mark = "" if mine == expected else " **≠**"
        lines.append(f"| {name} | {mine}{mark} | {expected} | {source} |")

    lines += ["", "## Across-repeat values that moved", "",
              "| Field | Fix | Current | Corrected | Ratio |", "|---|---|---|---|---|"]
    for path, fix, before, after in changed:
        if not path.startswith("/across_repeats"):
            continue
        ratio = (f"{after / before:.2f}×" if isinstance(before, (int, float))
                 and isinstance(after, (int, float)) and before else "")
        lines.append(f"| `{path[len('/across_repeats/'):]}` | {fix} | {before} | {after} | {ratio} |")
    lines += ["", "## Across-repeat fields added", "", "| Field | Fix | Value |", "|---|---|---|"]
    for path, fix, _, after in added:
        if path.startswith("/across_repeats"):
            lines.append(f"| `{path[len('/across_repeats/'):]}` | {fix} | {after} |")

    lines += ["", "## Per-repeat fields", "", "| Fix | Changed | Added | Removed |", "|---|---|---|---|"]
    per_repeat = {}
    for kind, rows in (("changed", changed), ("added", added), ("removed", removed)):
        for path, fix, _, _ in rows:
            if not path.startswith("/across_repeats"):
                per_repeat.setdefault(fix, {"changed": 0, "added": 0, "removed": 0})[kind] += 1
    for fix, counts in sorted(per_repeat.items()):
        lines.append(f"| {fix} | {counts['changed']} | {counts['added']} | {counts['removed']} |")
    lines.append("")
    lines.append("Per-repeat `chromium_wakes` lists shrink to the renderers "
                 "(removed rows are the non-renderer processes).")
    (HERE / "comparison.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:9]))
    return 1 if failures or check_failures else 0


if __name__ == "__main__":
    sys.exit(main())
