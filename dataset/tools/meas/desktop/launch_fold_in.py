#!/usr/bin/env python3
"""Write the launch phases' streams from the pooled landings (9.10 changelog D133, D136–D138).

launch_fold_in.py <artifacts-root> --source <tag> [--cpu-model "EPYC 7763"] [--out dataset/launch] [--check]

For each launch subject's entry, dataset/launch/launch-<entry>.json.gz: per pooled repeat, the run id, the phase's
length and its streams — the whole tree's, or for `renderer-hidden` each measured renderer's (D133) — each wake
[t_us from the phase's start, run_us, thread] with the thread an index into the repeat's comm list. Every same-machine
repeat obtained is pooled (pool.py's find_runs). The file is written byte-stable (gzip without a timestamp, sorted
keys), so --check exits 1 when a file differs from what the landings give.
"""

import argparse
import gzip
import io
import json
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # dataset/tools
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from meas.desktop.pool import find_runs, repeat_order  # noqa: E402

ENTRY = {"soffice": "office-writer", "thunderbird-send": "mail-client", "kdenlive": "video-editor",
         "mpv-video": "video-player", "mpv-audio": "audio-player", "element": "chat-client", "steam": "game-client",
         "chrome": "web-browser", "chrome-hidden": "renderer-hidden", "webrtc": "video-call"}


def streams_of(D, subject):
    """(phase_us, [stream, …], comms) from one landing's launch.summary.json and launch.events.tsv.gz."""
    summary = json.load(open(os.path.join(D, "launch.summary.json")))
    names = (sorted((k for k in summary["streams"] if k.startswith("renderer")), key=lambda k: int(k[len("renderer"):]))
             if subject == "chrome-hidden" else ["tree"])
    comms, index, by = [], {}, {n: [] for n in names}
    with gzip.open(os.path.join(D, "launch.events.tsv.gz"), "rt") as handle:
        next(handle)
        for line in handle:
            stream, t_us, run_us, _tid, _pid, comm, _role = line.rstrip("\n").split("\t")
            if stream not in by:
                continue
            if comm not in index:
                index[comm] = len(comms)
                comms.append(comm)
            by[stream].append([int(t_us), int(run_us), index[comm]])
    for s in by.values():
        s.sort()
    return round(summary["phase_s"] * 1e6), [by[n] for n in names], comms


def build(root, source, cpu_model):
    runs, _gated, _other, _probes = find_runs(root, cpu_model)
    out = {}
    for app, reps in sorted(runs.items()):
        if not app.startswith("launch-"):
            continue
        subject = app[len("launch-"):]
        entry = ENTRY[subject]
        repeats = []
        for k in sorted(reps, key=repeat_order):
            info = reps[k]
            phase_us, streams, comms = streams_of(info["dir"], subject)
            run_id = str((info["spec"].get("github_run") or {}).get("GITHUB_RUN_ID") or "")
            repeats.append({"repeat": str(k), "run_id": run_id, "phase_us": phase_us, "comms": comms, "streams": streams})
        out[f"launch-{entry}"] = {"entry": entry, "subject": app, "source": source, "repeats": repeats}
    return out


def encode(doc):
    raw = (json.dumps(doc, sort_keys=True, separators=(",", ":")) + "\n").encode()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as g:
        g.write(raw)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--source", required=True)
    ap.add_argument("--cpu-model", default="EPYC 7763")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(TOOLS), "launch"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    docs = build(a.root, a.source, a.cpu_model)
    if not docs:
        raise SystemExit("no launch landings found")
    differ = []
    os.makedirs(a.out, exist_ok=True)
    for name, doc in docs.items():
        path = os.path.join(a.out, f"{name}.json.gz")
        data = encode(doc)
        same = os.path.exists(path) and open(path, "rb").read() == data
        n = sum(len(s) for r in doc["repeats"] for s in r["streams"])
        print(f"{name}: {len(doc['repeats'])} repeats, {n} wakes, {len(data)} bytes{'' if same else ' (differs)'}")
        if a.check:
            if not same:
                differ.append(name)
        else:
            open(path, "wb").write(data)
    if a.check and differ:
        raise SystemExit(f"differ from the landings: {', '.join(differ)}")


if __name__ == "__main__":
    main()
