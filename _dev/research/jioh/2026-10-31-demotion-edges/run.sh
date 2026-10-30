#!/bin/bash
# run.sh OUT SIM FILE SLICE_US — the reference simulator on a core-set file under the
# primary boot default with only the top slice changed; writes OUT/FILE.SLICE.jsonl.
# Run from the repository root.
set -e
out=$1; sim=$2; f=$3; sl=$4
python3 - "$out" "$f" "$sl" <<'PY'
import json, sys
out, f, sl = sys.argv[1], sys.argv[2], int(sys.argv[3])
w = json.load(open(f"dataset/build/coreset-single/{f}.workload.json")); w["meta"] = {"id": f}
json.dump(w, open(f"{out}/{f}.json", "w"))
cfg = json.load(open("harness/boot-defaults/ostep.json")); cfg["params"]["timeslice_us"] = sl
json.dump({"workload_id": f, "condition": "fixed",
           "schedule": [{"t_us": 0, "config": cfg, "provenance": "fallback"}]},
          open(f"{out}/{f}.{sl}.sched", "w"))
PY
"$sim" --workload "$out/$f.json" --schedule "$out/$f.$sl.sched" --out-trace "$out/$f.$sl.jsonl" > /dev/null
