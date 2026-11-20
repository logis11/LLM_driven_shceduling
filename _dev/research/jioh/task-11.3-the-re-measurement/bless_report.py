#!/usr/bin/env python3
"""The second bless's report (the 11.3 spec, decision 10): over every manifest under dataset/ — the coreset's, the 78
sensitivity variants' and the five generated sets' — the artifacts whose bytes change beyond the library's hash
against HEAD's manifest (dataset/tools/beyond_hash.py's rule, applied to each), and the demands that move.

    python3 bless_report.py [--out bless-report.json]     (from the repository root, after `make -C dataset dataset
                                                            variants generated`, before the manifests are committed)

Every artifact pins the library by its git blob hash, so the library's edit changes every artifact's bytes; an
artifact whose bytes, the working tree's blob hash swapped back for HEAD's, hash to HEAD's manifest changed in nothing
but the hash."""
import argparse
import json
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "dataset" / "tools"))
from beyond_hash import beyond_hash, demand_moves  # noqa: E402

MANIFESTS = ["build.manifest.json", "build.variants.manifest.json", "build.transition-grid.manifest.json",
             "build.return-grid.manifest.json", "build.flap-stress.manifest.json",
             "build.distractor-grid.manifest.json", "build.familiarity-ladder.manifest.json"]


def git(*a):
    return subprocess.check_output(["git", *a], cwd=REPO / "dataset").decode()


def sha(entry):
    return entry if isinstance(entry, str) else entry["sha256"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parent / "bless-report.json"))
    args = ap.parse_args()
    new_blob = git("hash-object", "archetypes.yaml").strip()
    old_blob = git("rev-parse", "HEAD:./archetypes.yaml").strip()
    out = {"library_blob": {"head": old_blob, "working_tree": new_blob}, "manifests": {}}
    for name in MANIFESTS:
        head = json.loads(git("show", f"HEAD:./{name}"))
        new = json.loads((REPO / "dataset" / name).read_text())
        built = {}
        for rel, entry in new["artifacts"].items():
            b = (REPO / "dataset" / "build" / rel).read_bytes()
            built[rel] = b
        head_hashes = {rel: sha(e) for rel, e in head["artifacts"].items()}
        moved = beyond_hash(built, head_hashes, new_blob, old_blob)
        added = sorted(set(new["artifacts"]) - set(head["artifacts"]))
        gone = sorted(set(head["artifacts"]) - set(new["artifacts"]))
        demand = demand_moves(head.get("demand") or {}, new.get("demand") or {})
        out["manifests"][name] = {"artifacts": len(new["artifacts"]), "beyond_hash": moved, "added": added,
                                  "removed": gone, "demand_moves": demand}
        print(f"{name}: {len(moved)} of {len(new['artifacts'])} beyond the library's hash {moved}"
              + (f"; added {added}" if added else "") + (f"; removed {gone}" if gone else "")
              + f"; demand moves {demand or 'none'}")
    pathlib.Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
