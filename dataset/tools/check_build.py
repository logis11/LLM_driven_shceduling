#!/usr/bin/env python3
"""Verify the build against the committed manifests (9.18 spec, decision 6; 9.22 spec, decision 1).

Usage: check_build.py [--repo ROOT]

Two checks. The two manifests on disk equal their committed bytes (`git show
HEAD:<path>`): the build step rewrote them, so equality says the recompile
reproduces the committed set. And `dataset/build/` equals the union of
`dataset/build.manifest.json` (artifacts and reports) and
`dataset/build.variants.manifest.json` (variant artifacts): every file present
with the pinned hash, every pinned entry present, no file pinned by neither. A
missing build directory fails. Writes nothing.
"""

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

MANIFESTS = ("dataset/build.manifest.json", "dataset/build.variants.manifest.json")


def committed_bytes(root, rel):
    """The file's bytes at HEAD, or None when git has no such file."""
    done = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True)
    return done.stdout if done.returncode == 0 else None


def check_committed(root):
    """Returns error strings; empty when both manifests equal their committed bytes (9.22 spec, decision 1)."""
    errors = []
    for rel in MANIFESTS:
        path = root / rel
        if not path.is_file():
            errors.append(f"{rel}: missing (run `make dataset variants` first)")
            continue
        committed = committed_bytes(root, rel)
        if committed is None:
            errors.append(f"{rel}: not in git at HEAD")
        elif committed != path.read_bytes():
            errors.append(f"{rel}: the build wrote a manifest that differs from the committed one — "
                          "re-bless (commit it) if the change is intended")
    return errors


def expected_hashes(root):
    """{relpath under build/: sha256} from both manifests."""
    dataset = root / "dataset"
    expected = {}
    manifest = json.loads((dataset / "build.manifest.json").read_text(encoding="utf-8"))
    for section in ("artifacts", "reports"):
        expected.update(manifest.get(section) or {})
    variants = json.loads((dataset / "build.variants.manifest.json").read_text(encoding="utf-8"))
    for rel, record in (variants.get("artifacts") or {}).items():
        expected[rel] = record["sha256"] if isinstance(record, dict) else record
    return expected


def check(root):
    """Returns error strings; empty when build/ equals the manifests."""
    build_dir = root / "dataset" / "build"
    if not build_dir.is_dir():
        return [f"{build_dir.relative_to(root)}: missing (run `make dataset variants` first)"]
    expected = expected_hashes(root)
    errors = []
    on_disk = {p.relative_to(build_dir).as_posix(): p for p in sorted(build_dir.rglob("*")) if p.is_file()}
    for rel in sorted(set(expected) - set(on_disk)):
        errors.append(f"build/{rel}: pinned by a manifest, missing on disk")
    for rel in sorted(set(on_disk) - set(expected)):
        errors.append(f"build/{rel}: on disk, pinned by no manifest")
    for rel in sorted(set(on_disk) & set(expected)):
        digest = hashlib.sha256(on_disk[rel].read_bytes()).hexdigest()
        if digest != expected[rel]:
            errors.append(f"build/{rel}: sha256 {digest[:12]}… differs from the pinned {expected[rel][:12]}…")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=None)
    args = parser.parse_args()
    root = (pathlib.Path(args.repo).resolve() if args.repo
            else pathlib.Path(__file__).resolve().parents[2])
    errors = check_committed(root) + check(root)
    if errors:
        print(f"{len(errors)} build error(s):", file=sys.stderr)
        for message in errors:
            print(f"  - {message}", file=sys.stderr)
        return 1
    print(f"build verified ({len(expected_hashes(root))} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
