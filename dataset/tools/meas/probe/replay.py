#!/usr/bin/env python3
"""Replay key events at given intervals through xdotool.

replay.py <intervals-file> <window-id|active> <out.jsonl>
Each line of the intervals file is a gap in milliseconds before the next
key. Sends one xdotool key per gap, waiting on the monotonic clock, and logs
the requested and achieved send time per event. probe tooling for the 9.5
campaign (per-event replay; S4-05 documents xdotool's constant --delay only).
"""

import json
import subprocess
import sys
import time

gaps_path, window, out_path = sys.argv[1:4]
gaps = [float(line) for line in open(gaps_path) if line.strip()]
keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "space"]
target = [] if window == "active" else ["--window", window]
t0 = time.monotonic()
due = t0
with open(out_path, "w") as log:
    for i, gap in enumerate(gaps):
        due += gap / 1000.0
        while True:
            now = time.monotonic()
            if now >= due:
                break
            time.sleep(min(0.002, due - now))
        sent = time.monotonic()
        subprocess.run(["xdotool", "key"] + target + [keys[i % len(keys)]],
                       check=False)
        log.write(json.dumps({"i": i, "gap_ms": gap,
                              "due_us": int(due * 1e6),
                              "sent_us": int(sent * 1e6),
                              "done_us": int(time.monotonic() * 1e6)}) + "\n")
