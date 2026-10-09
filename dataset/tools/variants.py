#!/usr/bin/env python3
"""Build the RQ0 gate spec's sensitivity variants and write their manifest (9.14
decisions 10 and 12; dataset/variants.yaml).

Usage: variants.py [--check] [--sets NAME,…] [--repo ROOT]
  --check   rebuild and fail if dataset/build.variants.manifest.json would change
            (CI determinism gate; writes nothing)
  --sets    build the named sets only (the manifest then covers those alone; not
            for the committed manifest)

Every variant lands beside the blessed artifacts as
dataset/build/coreset-single/<base>@<set>.workload.json, lints clean against the
workload schema and the canonical invariants, and the manifest records its
SHA-256, its base's artifact hash from dataset/build.manifest.json, the set's
transform and parameters, and the inputs' hashes.
"""

import argparse
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from wlc.compiler import canonical_bytes  # noqa: E402
from wlc.linter import lint_canonical, load_schema  # noqa: E402
from wlc.variants import VariantError, build_all, load_spec, variant_id  # noqa: E402


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def build(root, only=None):
    """Returns (manifest, artifacts {relpath: bytes}, errors)."""
    root = pathlib.Path(root)
    dataset = root / "dataset"
    build_dir = dataset / "build" / "coreset-single"
    spec = load_spec(dataset / "variants.yaml")
    schema = load_schema(dataset / "schema" / "workload.schema.json")
    base_manifest = json.loads((dataset / "build.manifest.json").read_text(encoding="utf-8"))
    artifacts, records, errors = {}, {}, []
    try:
        for set_spec, base_id, canonical, report in build_all(spec, root, build_dir, only=only):
            vid = variant_id(base_id, set_spec["name"])
            errors.extend(lint_canonical(canonical, schema, name=vid))
            rel = f"coreset-single/{vid}.workload.json"
            data = canonical_bytes(canonical)
            artifacts[rel] = data
            base_rel = f"coreset-single/{base_id}.workload.json"
            params = {k: v for k, v in set_spec.items() if k not in ("name", "files", "reason")}
            records[rel] = {"set": set_spec["name"], "base": base_rel,
                            "base_sha256": base_manifest["artifacts"].get(base_rel),
                            "transform": params, "sha256": sha256(data)}
            if report is not None:
                records[rel]["utilization"] = round(report["utilization"], 4)
                if report.get("replay"):   # the trace-replay set: per task, the stream and the window's offset
                    records[rel]["replay"] = report["replay"]
    except (VariantError, OSError, KeyError, ValueError) as exc:
        errors.append(f"variants: {exc}")
    manifest = {
        "inputs": {
            "dataset/variants.yaml": sha256((dataset / "variants.yaml").read_bytes()),
            "dataset/archetypes.yaml": sha256((dataset / "archetypes.yaml").read_bytes()),
            "dataset/build.manifest.json": sha256((dataset / "build.manifest.json").read_bytes()),
        },
        "artifacts": {rel: records[rel] for rel in sorted(records)},
    }
    return manifest, artifacts, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--sets", default=None)
    ap.add_argument("--repo", default=None)
    args = ap.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])
    only = set(args.sets.split(",")) if args.sets else None

    manifest, artifacts, errors = build(root, only=only)
    if errors:
        print(f"{len(errors)} error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    manifest_path = root / "dataset" / "build.variants.manifest.json"
    if args.check:
        if not manifest_path.exists():
            print("no committed variants manifest to check against", file=sys.stderr)
            return 1
        if manifest_path.read_bytes() != manifest_bytes:
            print("build.variants.manifest.json drift: rebuilt variants do not match the committed manifest",
                  file=sys.stderr)
            return 1
        print(f"variants manifest verified ({len(artifacts)} artifacts)")
        return 0
    for rel, data in artifacts.items():
        out = root / "dataset" / "build" / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
    if only is None:
        manifest_path.write_bytes(manifest_bytes)
        print(f"wrote {len(artifacts)} variant artifacts + manifest")
    else:
        print(f"wrote {len(artifacts)} variant artifacts (sets {sorted(only)}; manifest not written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
