#!/usr/bin/env python3
"""Extract per-application input streams from SWELL-KW uLog XML files.

swell_streams.py <out-dir> <uLog.xml>...

For each file and each ControlApplication of interest, consecutive input
events (Keyboard: character / special key / key combination; Mouse: clicked
/ dragged / wheel turned) form segments; a segment breaks when an event of
another application intervenes. Output: one JSONL per (file, application)
under <out-dir>/<app>/<file-stem>.jsonl, one event per line with the gap
since the previous event of the same segment (ms), the segment index, the
kind, and for mouse events the cursor position, button and wheel amount;
plus <out-dir>/summary.json with counts and gap percentiles per application.
Only timing and positions are used downstream; key values are not exported
(9.5 changelog D4: the recording's keys are not replayed).
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

APPS = {"WINWORD": "word", "OUTLOOK": "outlook", "iexplore": "ie"}
KEY_ACTIONS = {"character", "special key", "key combination"}
MOUSE_ACTIONS = {"clicked": "click", "dragged": "drag", "wheel turned": "wheel"}


def parse_ts(text):
    # 2012-10-15T12:47:37.6634665Z — seven fractional digits; keep 6
    base, frac = text.rstrip("Z").split(".")
    return datetime.fromisoformat(base).timestamp() + int(frac[:6].ljust(6, "0")) / 1e6


def events(path):
    for _, el in ET.iterparse(path, events=("end",)):
        if el.tag != "Event":
            continue
        etype = el.findtext("EventType")
        action = el.findtext("EventAction")
        app = el.findtext("Control/ControlApplication") or ""
        kind = None
        if etype == "Keyboard" and action in KEY_ACTIONS:
            kind = "key"
        elif etype == "Mouse" and action in MOUSE_ACTIONS:
            kind = MOUSE_ACTIONS[action]
        if kind:
            yield {"t": parse_ts(el.findtext("TimeStamp")), "kind": kind, "app": app,
                   "x": int(el.findtext("MouseCursorX") or 0) if kind != "key" else None,
                   "y": int(el.findtext("MouseCursorY") or 0) if kind != "key" else None,
                   "button": el.findtext("MouseButton") if kind != "key" else None,
                   "wheel": int(el.findtext("MouseWheelTurnAmount") or 0) if kind == "wheel" else None}
        elif etype in ("Keyboard", "Mouse", "Other"):
            yield {"t": None, "kind": "other", "app": app}
        el.clear()


def pct(values, q):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return round(values[lo] + (values[hi] - values[lo]) * (k - lo), 1)


def main():
    out_dir, paths = sys.argv[1], sys.argv[2:]
    summary = {}
    for path in paths:
        stem = os.path.splitext(os.path.basename(path))[0]
        streams = {app: [] for app in APPS.values()}
        segment = {app: 0 for app in APPS.values()}
        last = {}
        current_app = None
        for ev in events(path):
            app = APPS.get(ev["app"])
            if ev["kind"] == "other":
                # a non-input event does not break a segment; an input event of another app does
                continue
            if app is None:
                current_app = None
                continue
            if current_app != app:
                if last.get(app) is not None:
                    segment[app] += 1
                current_app = app
                last[app] = None
            prev = last[app]
            gap = round((ev["t"] - prev) * 1000, 1) if prev is not None else None
            streams[app].append({"seg": segment[app], "gap_ms": gap, "kind": ev["kind"],
                                 "x": ev["x"], "y": ev["y"], "button": ev["button"], "wheel": ev["wheel"]})
            last[app] = ev["t"]
        for app, rows in streams.items():
            if not rows:
                continue
            os.makedirs(os.path.join(out_dir, app), exist_ok=True)
            with open(os.path.join(out_dir, app, stem + ".jsonl"), "w") as handle:
                for row in rows:
                    handle.write(json.dumps(row) + "\n")
            key_gaps = [r["gap_ms"] for r in rows if r["kind"] == "key" and r["gap_ms"] is not None]
            ptr_gaps = [r["gap_ms"] for r in rows if r["kind"] != "key" and r["gap_ms"] is not None]
            summary.setdefault(app, {})[stem] = {
                "events": len(rows), "keys": sum(r["kind"] == "key" for r in rows),
                "clicks": sum(r["kind"] == "click" for r in rows),
                "drags": sum(r["kind"] == "drag" for r in rows),
                "wheels": sum(r["kind"] == "wheel" for r in rows),
                "segments": segment[app] + 1,
                "span_s": round(sum(r["gap_ms"] or 0 for r in rows) / 1000, 1),
                "key_gap_ms": {"n": len(key_gaps), "p50": pct(key_gaps, .5), "p90": pct(key_gaps, .9),
                               "p99": pct(key_gaps, .99), "share_gt_1s": round(sum(g > 1000 for g in key_gaps) / len(key_gaps), 3) if key_gaps else None},
                "pointer_gap_ms": {"n": len(ptr_gaps), "p50": pct(ptr_gaps, .5), "p90": pct(ptr_gaps, .9)},
            }
    os.makedirs(out_dir, exist_ok=True)
    json.dump(summary, open(os.path.join(out_dir, "summary.json"), "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
