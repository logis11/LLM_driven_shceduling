#!/usr/bin/env python3
"""The outside-cause wakes of every census file summed by cause group, per section: PHP 8.3's FastCGI service
(`php-fpm`), PHP's session cleanup, `podman`, `sphinxsearch`, the runner's agent and provisioner, the tracer, the
workflow's steps (run.sh and the processes it starts), the Azure VM daemons and the other runner-only services.

  python3 -I by_cause.py <census.json> [<census.json> ...]
"""
import collections
import json
import sys

GROUPS = (("php-fpm", ("php8.3-fpm",)), ("PHP session cleanup", ("phpsessionclean", "PHP's session cleanup")),
          ("podman", ("podman",)), ("sphinxsearch", ("sphinxsearch",)),
          ("runner agent / provisioner", ("runner agent", "runner provisioner")), ("tracer (perf)", ("(tracer)",)),
          ("workflow step / run.sh", ("workflow step", "(run.sh)", "input driver")),
          ("Azure VM daemons", ("hyperv-daemons",)),
          ("other runner-only services", ("containerd", "docker.io", "multipath-tools", "chrony", "runc", "haveged",
                                          "walinuxagent", "irqbalance", "systemd-networkd", "clamav", "mono", "at (")))


def group(label):
    for g, keys in GROUPS:
        if any(k in label for k in keys):
            return g
    return "other: " + label


print("| section | campaign | k | wakes | outside | " + " | ".join(g for g, _ in GROUPS) + " |")
print("|---|---|---|---|---|" + "---|" * len(GROUPS))
for path in sys.argv[1:]:
    for sec, e in json.load(open(path)).items():
        c, n = collections.Counter(), 0
        for res in e["repeats"].values():
            for comp in res.values():
                n += comp["n"]
                for lab, x in comp["labels"].items():
                    if lab.startswith("outside: "):
                        c[group(lab[len("outside: "):])] += x
        other = {g: x for g, x in c.items() if g.startswith("other: ")}
        print(f"| {sec} | {e['campaign']} | {len(e['repeats'])} | {n} | {sum(c.values())} | "
              + " | ".join(str(c.get(g, 0)) for g, _ in GROUPS) + " |" + (f" {other}" if other else ""))
