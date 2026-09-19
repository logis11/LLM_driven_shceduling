#!/usr/bin/env python3
"""Each window's state per application across a campaign's runs.

status.py <family> [--since N] [--app APP[:N]]...

--since N: the campaign's first run number in the family. --app APP:N starts one application later (an application
restarted under a new design, 9.5 D28). Per application: landed (measured), in flight (queued or measuring),
gated only (every attempt stopped by the machine gate or failed), and failed attempts.
"""

import sys
from collections import defaultdict

import common


def collect(family, since=1, app_since=None):
    app_since = app_since or {}
    state = defaultdict(lambda: defaultdict(list))
    for r in common.runs(family, since):
        for j in common.jobs(family, r["databaseId"]):
            if r["number"] < app_since.get(j["app"], since):
                continue
            state[j["app"]][j["k"]].append(j)
    return state


def summary(windows):
    landed = sorted(k for k, js in windows.items() if any(j["state"] == "landed" for j in js))
    live = sorted(k for k, js in windows.items() if any(j["state"] in ("queued", "measuring") for j in js))
    gated = sorted(k for k, js in windows.items() if k not in landed and k not in live)
    failed = sorted(k for k, js in windows.items() if any(j["state"] == "failed" for j in js))
    return landed, live, gated, failed


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    family, since, app_since = a[0], 1, {}
    i = 1
    while i < len(a):
        if a[i] == "--since":
            since = int(a[i + 1]); i += 2
        elif a[i] == "--app":
            n, _, s = a[i + 1].partition(":"); app_since[n] = int(s) if s else since; i += 2
        else:
            raise SystemExit(__doc__)
    for app, windows in sorted(collect(family, since, app_since).items(), key=lambda kv: str(kv[0])):
        landed, live, gated, failed = summary(windows)
        print(f"{app or 'build':12} landed {landed}  in flight {live}  gated only {gated}" + (f"  failed {failed}" if failed else ""))


if __name__ == "__main__":
    main()
