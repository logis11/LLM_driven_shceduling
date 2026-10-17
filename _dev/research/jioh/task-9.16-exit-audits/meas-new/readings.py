#!/usr/bin/env python3
"""9.16: the burstiness and window readings (dataset/tools/meas/burstiness.py, windows.py) re-run on the two pools
9.15 handed over — `renderer-hidden`'s (`meas-ci:desktop:2026-10-05b`, 9.10 D156) and `video-editor`'s idle pool
(`meas-ci:interactive:2026-10-05`, 9.10 D146). The committed tools' own entry functions, two adjustments only:

- `video-editor`'s idle landings are named `meas-interactive-kdenlive-r<k>-idle` (the campaign's mode `idle`), while
  the tools' campaign family looks a carried repeat up as `…-full`; the lookup falls back to `…-idle`.
- windows.py's campaign family also reads `video-editor`'s driven and operation phases, which still come from 9.5's
  pool (`meas-ci:interactive:2026-09-18`) and were read there; only the idle phase is read here.

readings.py <artifacts root: <run id>/<landing> per carried repeat> <out dir>
"""

import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 5))
TOOLS = os.path.join(REPO, "dataset", "tools")
sys.path.insert(0, TOOLS)

from meas import burstiness as b, windows as w   # noqa: E402

_artifact_dir = b.artifact_dir


def artifact_dir(root, app, rep, run_id, mode="full"):
    try:
        return _artifact_dir(root, app, rep, run_id, mode)
    except SystemExit:
        if mode != "full":
            raise
        return _artifact_dir(root, app, rep, run_id, "idle")


def main():
    root, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    b.artifact_dir = artifact_dir
    w.DRIVEN_95, w.OPS_95 = (), ()
    burst = {"family": "9.16 re-run", "archetypes": {**b.desktop_entries(root, ("chrome-hidden",)),
                                                    **b.campaign_entries(root, ("kdenlive",))}}
    win = {"family": "9.16 re-run", "archetypes": {**w.desktop_entries(root, ("chrome-hidden",)),
                                                  **w.campaign_entries(root, ("kdenlive",))}}
    json.dump(burst, open(os.path.join(out, "burstiness.json"), "w"), indent=1)
    json.dump(win, open(os.path.join(out, "windows.json"), "w"), indent=1)
    open(os.path.join(out, "burstiness-tables.md"), "w").write(b.render(burst))
    open(os.path.join(out, "windows-tables.md"), "w").write(w.render(win))


if __name__ == "__main__":
    main()
