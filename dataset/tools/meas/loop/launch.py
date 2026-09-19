#!/usr/bin/env python3
"""Launch campaign jobs: write the trigger file, commit and push (the push is what starts the runs).

launch.py <first|added|retried|probe> <target>... [--dry]

A target is <family>/<app>:<k> (interactive, playback) or build:<k>; k is the repeat index — for work driven by recorded
input, the input window, which must already be committed (cut_windows.sh). Every job runs under the machine gate
(common.MACHINE). --dry prints the commit message and writes nothing.
"""

import sys
import time

import common


def main():
    args = [a for a in sys.argv[1:] if a != "--dry"]
    dry = "--dry" in sys.argv
    if len(args) < 2 or args[0] not in ("first", "added", "retried", "probe"):
        raise SystemExit(__doc__)
    targets = [common.parse_target(t) for t in args[1:]]
    if any(k is None or (common.FAMILIES[f]["apps"] and not a) for f, a, k in targets):
        raise SystemExit("every target needs a window or repeat index, and an app outside the build family")
    print(common.push_trigger(targets, args[0], dry=dry))
    if dry:
        return
    time.sleep(15)
    for fam in sorted({f for f, _, _ in targets}):
        r = common.runs(fam)[-1]
        print(f"{fam}: run #{r['number']} {r['databaseId']} {r['status']}")


if __name__ == "__main__":
    main()
