#!/usr/bin/env python3
"""Cut the per-repeat stimulus windows from extracted SWELL-KW streams.

build_windows.py <extracted-dir> <manifest.json> <out-dir> [--window-s 600] [--repeats 5]

<extracted-dir> is swell_streams.py's output (word/, outlook/, ie/ with one
JSONL per uLog file). Rule (9.5 changelog D12): per application, files of the
chosen conditions (word, ie: c1; outlook: c2 and c3) in participant order;
a segment or file boundary counts as one 2 000 ms gap; recorded time is
accumulated and repeat r takes the r-th window of --window-s seconds.
Output: <out-dir>/<app>-r<r>.jsonl with gap_ms resolved (seg = 0) so
replay_stream.py plays it as one stream, plus <out-dir>/windows.json
listing per window the source files, event counts and recorded span.
"""

import argparse
import json
import os
import re

CONDITIONS = {"word": {1}, "ie": {1}, "outlook": {2, 3}}
BOUNDARY_MS = 2000.0
RX = re.compile(r"^[ab]_pp(\d+)_c(\d)_?uLog_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("extracted"); ap.add_argument("manifest"); ap.add_argument("out")
    ap.add_argument("--window-s", type=float, default=600.0)
    ap.add_argument("--repeats", type=int, default=5)
    args = ap.parse_args()
    manifest = json.load(open(args.manifest))
    order = sorted(manifest["files"], key=lambda f: (f["pp"], f["cond"], f["name"]))
    os.makedirs(args.out, exist_ok=True)
    index = {}
    for app, conds in CONDITIONS.items():
        events = []  # (gap_ms, event, source)
        for f in order:
            if f["cond"] not in conds:
                continue
            stem = os.path.splitext(f["name"])[0]
            path = os.path.join(args.extracted, app, stem + ".jsonl")
            if not os.path.exists(path):
                continue
            last_seg = None
            first_in_file = True
            for line in open(path):
                ev = json.loads(line)
                if first_in_file or ev["seg"] != last_seg or ev["gap_ms"] is None:
                    gap = BOUNDARY_MS if events else 0.0
                else:
                    gap = ev["gap_ms"]
                first_in_file = False
                last_seg = ev["seg"]
                events.append((gap, ev, f["name"]))
        windows = [[] for _ in range(args.repeats)]
        elapsed = 0.0
        for gap, ev, src in events:
            elapsed += gap / 1000.0
            r = int(elapsed // args.window_s)
            if r >= args.repeats:
                break
            windows[r].append((gap if windows[r] else 0.0, ev, src))
        for r, win in enumerate(windows, start=1):
            out = os.path.join(args.out, f"{app}-r{r}.jsonl")
            with open(out, "w") as handle:
                for gap, ev, src in win:
                    row = {"gap_ms": round(gap, 1), "seg": 0, "kind": ev["kind"], "x": ev["x"], "y": ev["y"],
                           "button": ev["button"], "wheel": ev["wheel"]}
                    handle.write(json.dumps(row) + "\n")
            index[f"{app}-r{r}"] = {
                "sources": sorted({src for _, _, src in win}),
                "events": len(win), "keys": sum(ev["kind"] == "key" for _, ev, _ in win),
                "pointer": sum(ev["kind"] != "key" for _, ev, _ in win),
                "span_s": round(sum(g for g, _, _ in win) / 1000, 1),
            }
        print(app, "total recorded", round(elapsed, 0), "s over", len(events), "events;",
              "windows:", [index[f"{app}-r{r}"]["events"] for r in range(1, args.repeats + 1)])
    json.dump({"rule": "D12: c1 for word and ie, c2+c3 for outlook; participant order; 2000 ms per segment/file boundary; 600 s windows",
               "dataset": manifest["dataset"], "windows": index}, open(os.path.join(args.out, "windows.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
