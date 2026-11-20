#!/usr/bin/env python3
"""The finding step's builds (the 11.3 spec, decisions 1, 2 and 14): `c7-ml-train` compiled from a copy of the
library with one carried value at the lower bound of its interval and the other three at the library's values —
one build per value — and the two controls, the build with nothing moved and the build with all four moved.

    python3 finding_builds.py [--jobs N]

Each build's library copy goes to `finding/library/<build>/archetypes.yaml` and its compiled file to
`finding/build/<dir>/<id>.workload.json` beside this script (both local only, reproducible from this script). A
build carries the id of the file it stands for, since the simulator seeds its lottery draw from the workload id
(finding-first-run.json): each single-value build is `c7-ml-train`, in a directory of its own; the two controls
share `finding/build/controls/`, nothing moved as `c7-ml-train` and all four moved as `c7-ml-train@corner-low`.
The values are the four rows of `dataset/variants.yaml`'s `carried_values` on the two entries the file holds,
scaled as the corner sets scale them (dataset/tools/wlc/variants.py, `scaled_library`). Writes
`finding-builds.json`: each build's moved value, its library copy's and its compiled file's SHA-256, and the two
controls' bytes against the blessed artifacts (`dataset/build/coreset-single/c7-ml-train.workload.json` and
`c7-ml-train@corner-low.workload.json`). Exit 1 when a build does not lint or a control's bytes differ."""
import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "dataset" / "tools"))
from wlc.compiler import canonical_bytes  # noqa: E402
from wlc.linter import lint_canonical, load_schema  # noqa: E402
from wlc.variants import _compile_raw, _library_from, load_spec, scaled_library  # noqa: E402

BASE = "c7-ml-train"
BLESSED = REPO / "dataset" / "build" / "coreset-single"
OUT = HERE / "finding"
# decision 1's four values, keyed as dataset/variants.yaml's carried_values rows
VALUES = {
    "libuv-gap-low": {"entry": "code-editor", "component": "utility/libuv-worker", "table": "gap"},
    "libuv-run-low": {"entry": "code-editor", "component": "utility/libuv-worker", "table": "run"},
    "python3-run-low": {"entry": "cpu-batch", "program": "python3", "table": "python3_run"},
    "python3-block-low": {"entry": "cpu-batch", "program": "python3", "table": "python3_block"},
}
# the build with nothing moved, the four, and the build with all four moved: build -> (directory, id)
BUILDS = {"nothing-moved": ("controls", BASE), **{v: (v, BASE) for v in VALUES},
          "all-four-low": ("controls", f"{BASE}@corner-low")}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def carried_row(want):
    rows = [cv for cv in load_spec(REPO / "dataset" / "variants.yaml")["carried_values"]
            if all(cv.get(k) == v for k, v in want.items())]
    if len(rows) != 1:
        raise SystemExit(f"{want}: {len(rows)} carried_values rows, one expected")
    return rows[0]


def moved_rows(build):
    if build == "nothing-moved":
        return []
    if build == "all-four-low":
        return [carried_row(v) for v in VALUES.values()]
    return [carried_row(VALUES[build])]


def build_one(build):
    rows = moved_rows(build)
    lib_dir = OUT / "library" / build
    work = OUT / "work" / build
    for d in (lib_dir, work):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    lib_doc = yaml.safe_load((REPO / "dataset" / "archetypes.yaml").read_text(encoding="utf-8"))
    library = _library_from(scaled_library(lib_doc, rows, "low"), lib_dir)
    raw = yaml.safe_load((REPO / "dataset" / "timelines" / "coreset" / f"{BASE}.timeline.yaml")
                         .read_text(encoding="utf-8"))
    base_meta = json.loads((BLESSED / f"{BASE}.workload.json").read_text(encoding="utf-8"))["meta"]
    canonical, _ = _compile_raw(raw, library, work, BASE)
    sub, wid = BUILDS[build]
    canonical["meta"] = dict(base_meta, id=wid)          # the base's provenance, as the variants tool sets it
    errors = lint_canonical(canonical, load_schema(REPO / "dataset" / "schema" / "workload.schema.json"), name=wid)
    data = canonical_bytes(canonical)
    (OUT / "build" / sub).mkdir(parents=True, exist_ok=True)
    (OUT / "build" / sub / f"{wid}.workload.json").write_bytes(data)
    shutil.rmtree(work, ignore_errors=True)
    return {"build": build, "build_dir": str((OUT / "build" / sub).relative_to(REPO)), "workload_id": wid,
            "moved": [{k: r[k] for k in ("entry", "component", "program", "table", "half_width") if k in r}
                      for r in rows],
            "library_sha256": sha256((lib_dir / "archetypes.yaml").read_bytes()),
            "sha256": sha256(data), "lint_errors": errors}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--jobs", type=int, default=len(BUILDS))
    args = ap.parse_args()
    shutil.rmtree(OUT / "build", ignore_errors=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        builds = list(pool.map(build_one, BUILDS))
    shutil.rmtree(OUT / "work", ignore_errors=True)
    by = {b["build"]: b for b in builds}
    controls = {}
    for build, blessed in (("nothing-moved", f"{BASE}.workload.json"),
                           ("all-four-low", f"{BASE}@corner-low.workload.json")):
        blessed_sha = sha256((BLESSED / blessed).read_bytes())
        controls[build] = {"blessed": f"dataset/build/coreset-single/{blessed}", "blessed_sha256": blessed_sha,
                           "identical": by[build]["sha256"] == blessed_sha}
    out = {"base": BASE, "library": "dataset/archetypes.yaml",
           "library_sha256": sha256((REPO / "dataset" / "archetypes.yaml").read_bytes()),
           "builds": builds, "controls": controls}
    (HERE / "finding-builds.json").write_text(json.dumps(out, indent=2) + "\n")
    bad = [b["build"] for b in builds if b["lint_errors"]] + [k for k, c in controls.items() if not c["identical"]]
    for b in builds:
        print(f"{b['build']} ({b['build_dir']}/{b['workload_id']}): {b['sha256'][:12]} lint "
              f"{'clean' if not b['lint_errors'] else b['lint_errors']}")
    for k, c in controls.items():
        print(f"control {k}: {'identical' if c['identical'] else 'DIFFERS'} to {c['blessed']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
