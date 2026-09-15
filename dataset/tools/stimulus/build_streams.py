#!/usr/bin/env python3
"""Build the dataset's replayed input streams (9.5 changelog D18) from
swell_streams.py's extraction of the SWELL-KW uLog files.

build_streams.py <extracted-dir> <manifest.json> <out-dir>

One JSONL per stream — swell-word-c1, swell-outlook-c23, swell-ie-c1 — with
every input event (keys and pointer events, D12) of the chosen conditions in
participant order, a segment or file boundary counting as one 2 000 ms gap
(the same rule as the campaign's build_windows.py). Rows: t_us (cumulative
recorded time), kind. Key values and cursor positions are not carried: the
compiler needs timing only. <out-dir>/streams.json indexes the streams with
their sources, counts and spans.
"""

import json
import os
import re
import sys

STREAMS = {"swell-word-c1": ("word", {1}), "swell-outlook-c23": ("outlook", {2, 3}), "swell-ie-c1": ("ie", {1})}
BOUNDARY_MS = 2000.0


def main():
    extracted, manifest_path, out = sys.argv[1:4]
    manifest = json.load(open(manifest_path))
    order = sorted(manifest["files"], key=lambda f: (f["pp"], f["cond"], f["name"]))
    os.makedirs(out, exist_ok=True)
    index = {}
    for sid, (app, conds) in STREAMS.items():
        t_ms = 0.0
        n = 0
        kinds = {}
        sources = []
        with open(os.path.join(out, sid + ".jsonl"), "w") as handle:
            for f in order:
                if f["cond"] not in conds:
                    continue
                path = os.path.join(extracted, app, os.path.splitext(f["name"])[0] + ".jsonl")
                if not os.path.exists(path):
                    continue
                sources.append(f["name"])
                last_seg, first = None, True
                for line in open(path):
                    ev = json.loads(line)
                    if first or ev["seg"] != last_seg or ev["gap_ms"] is None:
                        gap = BOUNDARY_MS if n else 0.0
                    else:
                        gap = ev["gap_ms"]
                    first, last_seg = False, ev["seg"]
                    t_ms += gap
                    handle.write(json.dumps({"t_us": int(round(t_ms * 1000)), "kind": ev["kind"]}) + "\n")
                    n += 1
                    kinds[ev["kind"]] = kinds.get(ev["kind"], 0) + 1
        index[sid] = {"application": app, "conditions": sorted(conds), "files": len(sources), "sources": sources,
                      "events": n, "kinds": kinds, "span_s": round(t_ms / 1000, 1)}
        print(sid, n, "events", round(t_ms / 1000), "s", len(sources), "files")
    json.dump({"dataset": manifest["dataset"], "licence": manifest.get("licence"),
               "rule": "keys and pointer events of the named conditions, participant order, 2000 ms per segment or file boundary (D12, D18)",
               "streams": index}, open(os.path.join(out, "streams.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
