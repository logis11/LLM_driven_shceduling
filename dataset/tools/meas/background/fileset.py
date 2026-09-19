#!/usr/bin/env python3
"""The file set of the 9.7 campaign's `borg` and `7z` jobs (method §2; changelog D6, D7).

fileset.py manifest <set-dir> <out.tsv.gz>          write the manifest — path, size, SHA-256 per file, sorted by path —
                                                    and print its digest (SHA-256 of the uncompressed text), the pin
                                                    a later job's tree is verified against
fileset.py verify <set-dir> <manifest.tsv.gz>       the tree against a manifest file; prints a key=value summary, exit 1 on a mismatch
fileset.py setcheck <manifest.tsv.gz>               the pre-registered set check (D7), key=value
fileset.py change <set-dir> <stash-dir> <out.json>  apply the repeat backup's change set (D6), originals kept in the stash
fileset.py restore <set-dir> <stash-dir> <change.json>   undo it: originals back, new files removed

The change set's size follows Cumulus's personal-machine trace (T9-S1-05: 10.3 MB new and 29.9 MB changed per day over
a 2.37 GB home directory), scaled to the set: new files totalling NEW_SHARE of its bytes and changed files totalling
CHANGED_SHARE. Which files change, how and the new files' content are design, drawn from SEED: the changed files in a
seeded order over the sorted file list, each taken when it still fits under the target, in each one contiguous range — length
uniform in [1, size], offset uniform over the rest — rewritten with seeded random bytes, the file's length kept; new
files of seeded random bytes, their sizes drawn from the set's own file sizes until the target is reached (the last
one cut to it), each in a seeded choice among the set's directories. The same SEED gives every repeat the same change.
"""

import gzip
import hashlib
import json
import os
import random
import shutil
import statistics
import sys
from concurrent.futures import ProcessPoolExecutor

NEW_SHARE = 10.3 / 2370      # T9-S1-05, MB new per day over the 2.37 GB home directory
CHANGED_SHARE = 29.9 / 2370  # T9-S1-05, MB changed per day
SEED = 97_2026_09_19         # design
BIG = (30 * 10**6, 30 * 2**20)   # the 30 MB of T9-S1-02, read both ways (the paper does not define MB)
BLOCK = 1 << 20


def files_of(root):
    out = []
    for d, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(d, f)
            if os.path.isfile(p) and not os.path.islink(p):
                out.append(os.path.relpath(p, root))
    return sorted(out)


def dirs_of(root):
    out = [""]
    for d, dirs, _files in os.walk(root):
        dirs.sort()
        out.extend(os.path.relpath(os.path.join(d, x), root) for x in dirs)
    return sorted(out)


def _hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(BLOCK)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _entry(args):
    root, rel = args
    p = os.path.join(root, rel)
    return rel, os.path.getsize(p), _hash(p)


def scan(root, workers=None):
    rels = files_of(root)
    n = workers or (len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count())
    with ProcessPoolExecutor(max_workers=n) as ex:
        return list(ex.map(_entry, [(root, r) for r in rels], chunksize=64))


def manifest_text(entries):
    return "".join(f"{rel}\t{size}\t{sha}\n" for rel, size, sha in sorted(entries))


def write_manifest(entries, path):
    text = manifest_text(entries)
    with gzip.open(path, "wt") as f:
        f.write(text)
    return hashlib.sha256(text.encode()).hexdigest()


def read_manifest(path):
    out = []
    with gzip.open(path, "rt") if path.endswith(".gz") else open(path) as f:
        for line in f:
            rel, size, sha = line.rstrip("\n").split("\t")
            out.append((rel, int(size), sha))
    return out


def verify(root, manifest):
    want = {rel: (size, sha) for rel, size, sha in manifest}
    have = {rel: (size, sha) for rel, size, sha in scan(root)}
    missing = sorted(set(want) - set(have))
    extra = sorted(set(have) - set(want))
    differ = sorted(r for r in set(want) & set(have) if want[r] != have[r])
    return {"files": len(have), "bytes": sum(s for s, _ in have.values()), "missing": len(missing), "extra": len(extra),
            "differ": len(differ), "ok": not (missing or extra or differ), "first_problems": (missing + extra + differ)[:10]}


def set_check(manifest):
    """D7's pre-registered check: the median file size and the share of bytes in files over 30 MB."""
    sizes = [s for _, s, _ in manifest]
    total = sum(sizes)
    out = {"files": len(sizes), "bytes": total, "median_file_bytes": statistics.median(sizes) if sizes else None}
    for cut, name in zip(BIG, ("30e6", "30MiB")):
        out[f"share_bytes_over_{name}"] = round(sum(s for s in sizes if s > cut) / total, 4) if total else None
    return out


def plan_change(entries, dirs, seed=SEED):
    """The change set for a tree given as (rel, size) entries and its directories: {changed: [{path, size, offset,
    length}], new: [{path, size}], targets}."""
    rng = random.Random(seed)
    total = sum(s for _, s in entries)
    t_changed, t_new = round(total * CHANGED_SHARE), round(total * NEW_SHARE)
    order = [e for e in sorted(entries) if e[1] > 0]
    rng.shuffle(order)
    changed, acc = [], 0
    for rel, size in order:
        if acc + size > t_changed:   # a file that would overshoot the target is passed over
            continue
        length = rng.randint(1, size)
        offset = rng.randint(0, size - length)
        changed.append({"path": rel, "size": size, "offset": offset, "length": length})
        acc += size
    sizes = sorted(s for _, s in entries if s > 0)
    new, acc, i = [], 0, 0
    while acc < t_new and sizes:
        size = min(rng.choice(sizes), t_new - acc)
        d = rng.choice(dirs)
        new.append({"path": os.path.join(d, f"change-{seed}-{i:05d}.bin") if d else f"change-{seed}-{i:05d}.bin", "size": size})
        acc += size
        i += 1
    return {"seed": seed, "set_bytes": total, "target_changed_bytes": t_changed, "target_new_bytes": t_new,
            "changed_file_bytes": sum(c["size"] for c in changed), "rewritten_bytes": sum(c["length"] for c in changed),
            "new_bytes": sum(n["size"] for n in new), "changed": changed, "new": new}


def _random_bytes(rng, n):
    return rng.randbytes(n)


def apply_change(root, stash, plan):
    rng = random.Random(plan["seed"] + 1)
    for c in plan["changed"]:
        src = os.path.join(root, c["path"])
        dst = os.path.join(stash, c["path"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        with open(src, "r+b") as f:
            f.seek(c["offset"])
            left = c["length"]
            while left:
                n = min(left, BLOCK)
                f.write(_random_bytes(rng, n))
                left -= n
    for n in plan["new"]:
        p = os.path.join(root, n["path"])
        with open(p, "wb") as f:
            left = n["size"]
            while left:
                k = min(left, BLOCK)
                f.write(_random_bytes(rng, k))
                left -= k


def restore_change(root, stash, plan):
    for n in plan["new"]:
        p = os.path.join(root, n["path"])
        if os.path.exists(p):
            os.remove(p)
    for c in plan["changed"]:
        shutil.copy2(os.path.join(stash, c["path"]), os.path.join(root, c["path"]))


def _kv(d, prefix=""):
    for k, v in d.items():
        if not isinstance(v, (list, dict)):
            print(f"{prefix}{k}={v}")


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 2
    cmd = a[0]
    if cmd == "manifest":
        entries = scan(a[1])
        digest = write_manifest(entries, a[2])
        print(f"files={len(entries)}\nbytes={sum(s for _, s, _ in entries)}\nmanifest_sha256={digest}")
        return 0
    if cmd == "verify":
        r = verify(a[1], read_manifest(a[2]))
        _kv(r)
        print("first_problems=" + ",".join(r["first_problems"]))
        return 0 if r["ok"] else 1
    if cmd == "setcheck":
        _kv(set_check(read_manifest(a[1])))
        return 0
    if cmd == "change":
        root, stash, out = a[1], a[2], a[3]
        rels = files_of(root)
        plan = plan_change([(r, os.path.getsize(os.path.join(root, r))) for r in rels], dirs_of(root))
        apply_change(root, stash, plan)
        json.dump(plan, open(out, "w"), indent=1)
        _kv({k: v for k, v in plan.items() if k not in ("changed", "new")})
        print(f"changed_files={len(plan['changed'])}\nnew_files={len(plan['new'])}")
        return 0
    if cmd == "restore":
        restore_change(a[1], a[2], json.load(open(a[3])))
        print("restored=1")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
