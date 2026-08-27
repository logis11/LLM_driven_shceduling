#!/usr/bin/env python3
"""Record the runner spec (building-plan §7: machine-relative absolutes rank
as convention-informed-by-measurement and carry this record)."""

import json
import os
import platform
import sys
import time


def first_match(path, prefix):
    try:
        with open(path) as handle:
            for line in handle:
                if line.startswith(prefix):
                    return line.split(":", 1)[1].strip()
    except OSError:
        return None
    return None


def os_release():
    info = {}
    try:
        with open("/etc/os-release") as handle:
            for line in handle:
                if "=" in line:
                    key, _, value = line.strip().partition("=")
                    info[key] = value.strip('"')
    except OSError:
        pass
    return {k: info.get(k) for k in ("ID", "VERSION_ID", "PRETTY_NAME")}


def main():
    spec = {
        "recorded_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "uname": " ".join(platform.uname()),
        "nproc": os.cpu_count(),
        "cpu_model": first_match("/proc/cpuinfo", "model name"),
        "mem_total": first_match("/proc/meminfo", "MemTotal"),
        "os_release": os_release(),
        "github_run": {k: os.environ.get(k) for k in
                       ("GITHUB_WORKFLOW", "GITHUB_RUN_ID", "GITHUB_RUN_NUMBER",
                        "GITHUB_SHA", "GITHUB_JOB")},
    }
    json.dump(spec, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
