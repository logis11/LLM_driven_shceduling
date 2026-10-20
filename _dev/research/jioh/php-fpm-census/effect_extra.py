#!/usr/bin/env python3
"""The carried values that are CPU sums over the tree, not per-component wake counts: the playback entries' cycle
work (`cycle_run`) and period, the per-input run (`input_run`), the compile job's member steps and make's dispatch,
the batch programs' runs between blocks and the block after each. Removing an outside-cause wake removes at most its
run from the sum, so each value's shift is bounded by the outside-cause wakes' run against the run the value sums
(the cycle work and the input run over the pooled record's own totals; the build steps and the batch runs over the
role's or program's whole run in the phase), and a count-based mean (the batch runs, the blocks) by the outside-cause
wakes against the runs. The stated half-widths are the pooled records'.

  python3 -I effect_extra.py <census dir> > effect-extra.json
"""

import json
import os
import sys

RES = "/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/_dev/research/jioh"
P95 = os.path.join(RES, "task-9.5-interactive-typing", "campaign")
POOL = {"video-player": (os.path.join(P95, "results-same-machine", "pool-mpv-video.json"), "mpv-video"),
        "audio-player": (os.path.join(P95, "results-same-machine", "pool-mpv-audio.json"), "mpv-audio"),
        "video-call": (os.path.join(P95, "results-re-measured", "pool-webrtc.json"), "webrtc"),
        "office-writer": (os.path.join(P95, "results-same-machine", "pool-soffice.json"), "soffice"),
        "code-editor": (os.path.join(P95, "results-re-measured", "pool-code.json"), "code"),
        "web-browser": (os.path.join(P95, "results-re-measured", "pool-chrome.json"), "chrome"),
        "mail-client": (os.path.join(P95, "results-re-measured", "pool-thunderbird-send.json"), "thunderbird-send")}


def gone(c, classes):
    return (sum(c["classes"].get(x, {}).get("n", 0) for x in classes),
            sum(c["classes"].get(x, {}).get("run", 0.0) for x in classes))


def main():
    d = sys.argv[1]
    out = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".json") or f.startswith("effect"):
            continue
        for sec, e in json.load(open(os.path.join(d, f))).items():
            field = e.get("field")
            entry = sec.split()[0]
            if field in ("cycle", "input_run"):
                pool_path, app = POOL[entry]
                ph = json.load(open(pool_path))["runs"][app]
                q = ph["stability"]["quantities"]
                reps = e["repeats"]
                n = sum(r["tree"]["n"] for r in reps.values())
                o, orun = map(sum, zip(*[gone(r["tree"], ("outside",)) for r in reps.values()]))
                u, urun = map(sum, zip(*[gone(r["tree"], ("outside", "harness-python")) for r in reps.values()]))
                seg = sum(r["tree"]["segments_run"] for r in reps.values())
                row = {"section": sec, "campaign": e["campaign"], "field": field, "k": len(reps), "wakes": n,
                       "outside": o, "outside_run_ms": orun, "outside_upper": u, "outside_upper_run_ms": urun,
                       "tree_run_ms": seg, "per_repeat": [gone(reps[k]["tree"], ("outside",))[0] for k in reps]}
                if field == "cycle":
                    work = q["play cycle work mean (ms)"]
                    total = work["mean"] * sum(ph["phases"]["play"]["cycle"]["cycles"])
                    row.update(value="cycle work mean (ms)", mean=work["mean"], half_width=work["half_width"],
                               shift_bound=-orun / total, shift_bound_upper=-urun / total)
                else:
                    ir = q["input_run mean, SWELL-KW (ms)"]
                    total = ir["mean"] * sum(ph["phases"]["driven"]["per_input"]["events"])
                    row.update(value="input_run mean, SWELL-KW (ms)", mean=ir["mean"], half_width=ir["half_width"],
                               shift_bound=-orun / total, shift_bound_upper=-urun / total)
                out.append(row)
            elif sec in ("file-archiver", "game-download"):
                reps = e["repeats"]
                for prog in sorted({p for r in reps.values() for p in r}):
                    cs = [r[prog] for r in reps.values() if prog in r]
                    n, run = sum(c["n"] for c in cs), sum(c["run"] for c in cs)
                    o, orun = map(sum, zip(*[gone(c, ("outside",)) for c in cs]))
                    u, urun = map(sum, zip(*[gone(c, ("outside", "harness-python")) for c in cs]))
                    runs = sum(c.get("batch_runs", 0) for c in cs)
                    out.append({"section": sec, "campaign": e["campaign"], "program": prog, "k": len(cs), "wakes": n,
                                "outside": o, "outside_upper": u, "outside_run_ms": orun, "run_ms": run,
                                "batch_runs": runs, "run_share": orun / run if run else None,
                                "count_share": u / runs if runs else None,
                                "per_repeat": [gone(c, ("outside",))[0] for c in cs]})
            elif sec.startswith("compiler-child"):
                reps = e["repeats"]
                for role in sorted({p for r in reps.values() for p in r}):
                    cs = [r[role] for r in reps.values() if role in r]
                    n, run = sum(c["n"] for c in cs), sum(c["run"] for c in cs)
                    o, orun = map(sum, zip(*[gone(c, ("outside",)) for c in cs]))
                    u, urun = map(sum, zip(*[gone(c, ("outside", "harness-python")) for c in cs]))
                    out.append({"section": sec, "campaign": e["campaign"], "role": role, "k": len(cs), "wakes": n,
                                "outside": o, "outside_upper": u, "outside_run_ms": orun, "run_ms": run,
                                "run_share": orun / run if run else None, "per_repeat": [gone(c, ("outside",))[0] for c in cs]})
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
