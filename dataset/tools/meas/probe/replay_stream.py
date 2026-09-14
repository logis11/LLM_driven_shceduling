#!/usr/bin/env python3
"""Replay an extracted SWELL-KW stream (swell_streams.py JSONL) through xdotool.

replay_stream.py <stream.jsonl> <window-id> <out.jsonl> [--seconds N]
    [--kinds key,click,drag,wheel] [--motion-ms M] [--rec-size WxH]

Events are issued at their recorded gaps on the monotonic clock; segment
breaks (a change of `seg`) are joined with a fixed 2 000 ms gap, since the
recording's time between segments belonged to another application. Keys are
a fixed letter cycle (D4: timing only). Pointer events go to the recorded
cursor position scaled from --rec-size (default 1600x1200: the recordings' cursor range is 0–1599 × 0–1197) into the target
window's geometry; a click is xdotool `click 1`, a drag is mousedown, a move
to the next event's position, mouseup; a wheel is `click 4`/`click 5` repeated by the
recorded amount (unit counts 1–3 in the recordings; sign gives direction). With --motion-ms M, the move preceding a
pointer event is interpolated in steps every M ms (design, D5's open item);
without it the pointer jumps at the event's time. Stops after --seconds of
recorded time or at the stream's end. Log: one line per event with due and
sent times.
"""

import argparse
import json
import subprocess
import time

KEYS = list("abcdefghijklmnopqrstuvwxyz") + ["space"]


def xdo(*args):
    subprocess.run(["xdotool", *map(str, args)], check=False)


def geometry(window):
    out = subprocess.run(["xdotool", "getwindowgeometry", "--shell", window],
                         capture_output=True, text=True, check=False).stdout
    geo = dict(line.split("=") for line in out.split() if "=" in line)
    return int(geo.get("X", 0)), int(geo.get("Y", 0)), int(geo.get("WIDTH", 1280)), int(geo.get("HEIGHT", 800))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stream"); ap.add_argument("window"); ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=None)
    ap.add_argument("--kinds", default="key,click,drag,wheel")
    ap.add_argument("--motion-ms", type=float, default=0)
    ap.add_argument("--rec-size", default="1600x1200")
    ap.add_argument("--seg-gap-ms", type=float, default=2000)
    args = ap.parse_args()
    kinds = set(args.kinds.split(","))
    rw, rh = (int(v) for v in args.rec_size.split("x"))
    wx, wy, ww, wh = geometry(args.window)

    def pos(ev):
        x = wx + int((ev["x"] or 0) * ww / rw)
        y = wy + int((ev["y"] or 0) * wh / rh)
        return max(wx, min(wx + ww - 1, x)), max(wy, min(wy + wh - 1, y))

    events = [json.loads(line) for line in open(args.stream) if line.strip()]
    xdo("windowactivate", "--sync", args.window)
    t0 = time.monotonic()
    due = t0
    elapsed = 0.0
    last_seg = None
    cur = pos({"x": rw // 2, "y": rh // 2})
    n_key = 0
    with open(args.out, "w") as log:
        for i, ev in enumerate(events):
            gap = ev["gap_ms"] if (ev["gap_ms"] is not None and ev["seg"] == last_seg) else (0 if last_seg is None else args.seg_gap_ms)
            last_seg = ev["seg"]
            elapsed += gap / 1000.0
            if args.seconds is not None and elapsed > args.seconds:
                break
            due += gap / 1000.0
            if ev["kind"] not in kinds:
                continue
            target = pos(ev) if ev["kind"] != "key" else None
            if target and args.motion_ms > 0:
                steps = max(1, int(min(gap, 400) / args.motion_ms))
                for s in range(1, steps + 1):
                    t_step = due - (steps - s) * args.motion_ms / 1000.0
                    while time.monotonic() < t_step:
                        time.sleep(0.001)
                    xdo("mousemove", cur[0] + (target[0] - cur[0]) * s // steps, cur[1] + (target[1] - cur[1]) * s // steps)
            while time.monotonic() < due:
                time.sleep(min(0.002, due - time.monotonic()))
            sent = time.monotonic()
            if ev["kind"] == "key":
                xdo("key", KEYS[n_key % len(KEYS)]); n_key += 1
            elif ev["kind"] == "click":
                xdo("mousemove", *target, "click", 1); cur = target
            elif ev["kind"] == "drag":
                xdo("mousemove", *cur, "mousedown", 1, "mousemove", *target, "mouseup", 1); cur = target
            elif ev["kind"] == "wheel":
                units = int(ev.get("wheel") or 0)
                xdo("mousemove", *target, "click", "--repeat", max(1, abs(units)), 4 if units >= 0 else 5); cur = target
            log.write(json.dumps({"i": i, "kind": ev["kind"], "gap_ms": gap, "due_us": int(due * 1e6),
                                  "sent_us": int(sent * 1e6), "done_us": int(time.monotonic() * 1e6)}) + "\n")


if __name__ == "__main__":
    main()
