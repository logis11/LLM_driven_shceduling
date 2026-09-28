#!/usr/bin/env python3
"""Which compiled artifacts change beyond the library's hash, and which demands move, against HEAD.

Every artifact pins the library by its git blob hash (wlc/library.py, `git_blob_hex`), so any edit to
archetypes.yaml changes every artifact's bytes. After compile.py: each artifact with the working tree's library blob
hash swapped back for HEAD's, hashed against HEAD's manifest — the ones that still differ changed beyond the hash —
and each demand in the manifest that differs from HEAD's. The changelogs' "N of 100 artifacts changing beyond the
library's hash" and their demand moves are this report.

beyond_hash.py   (from dataset/)
"""

import hashlib
import json
import os
import subprocess
import sys


def beyond_hash(built, head_hashes, new_blob, old_blob):
    """built: {rel: bytes} as compiled; head_hashes: {rel: sha256} of HEAD's manifest. The rels whose bytes, the new
    library blob hash replaced by the old, still hash other than HEAD's."""
    return sorted(rel for rel, b in built.items()
                  if hashlib.sha256(b.replace(new_blob.encode(), old_blob.encode())).hexdigest() != head_hashes.get(rel))


def demand_moves(head, new):
    """{file: (HEAD's demand, the new one)} for every demand that differs."""
    return {k: (head.get(k), v) for k, v in new.items() if head.get(k) != v}


def main():
    git = lambda *a: subprocess.check_output(["git", *a]).decode()
    new_blob = git("hash-object", "archetypes.yaml").strip()
    old_blob = git("rev-parse", "HEAD:./archetypes.yaml").strip()
    head = json.loads(git("show", "HEAD:./build.manifest.json"))
    new = json.load(open("build.manifest.json"))
    built = {}
    for rel in head["artifacts"]:
        b = open(os.path.join("build", rel), "rb").read()
        if hashlib.sha256(b).hexdigest() != new["artifacts"][rel]:
            sys.exit(f"{rel}: build/ does not match build.manifest.json; recompile first")
        built[rel] = b
    moved = beyond_hash(built, head["artifacts"], new_blob, old_blob)
    print(f"{len(moved)} of {len(head['artifacts'])} artifacts change beyond the library's hash: {moved}")
    dd = demand_moves(head["demand"], new["demand"])
    print("demand changes:", dd if dd else "none")


if __name__ == "__main__":
    main()
