#!/usr/bin/env python3
"""hippocamp.py <repo> <revision> <tree> <dest> <listing.tsv> — the Tracker campaign's file set (9.10 D66–D68).

Lists <tree> of the Hugging Face dataset <repo> at <revision> (the tree API, recursive), downloads every file into
<dest> keeping the tree's relative paths, and checks each against the listing: its size, and its hash — the SHA-256
the listing gives a Git LFS file, or the Git blob SHA-1 of any other file. Each file is written beside its final
name and renamed once checked. Prints key=value lines (files, bytes, directories, failed, verified) for run.sh's
record; the listing TSV holds path, size, hash kind, hash and the outcome per file. Standard library only: it runs
with the runner's own Python on the harness CPUs.
"""

import concurrent.futures
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://huggingface.co/api/datasets/{repo}/tree/{rev}/{path}?recursive=true"
RESOLVE = "https://huggingface.co/datasets/{repo}/resolve/{rev}/{path}"
THREADS, TRIES, CHUNK = 8, 6, 1 << 20


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "meas-9.10-tracker"})
    return urllib.request.urlopen(req, timeout=120)


def listing(repo, rev, tree):
    """Every entry under <tree>, following the API's Link pagination."""
    url, out = API.format(repo=repo, rev=rev, path=urllib.parse.quote(tree)), []
    while url:
        for k in range(TRIES):
            try:
                with get(url) as r:
                    out += json.load(r)
                    nxt = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get("Link") or "")
                    url = nxt.group(1) if nxt else None
                break
            except Exception:
                if k == TRIES - 1:
                    raise
                time.sleep(5 * (k + 1))
    return out


def fetch(repo, rev, entry, root, dest):
    rel = entry["path"][len(root):].lstrip("/")
    path = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lfs = entry.get("lfs")
    kind, want = ("sha256", lfs["oid"]) if lfs else ("git-sha1", entry["oid"])
    size = entry["size"]
    url = RESOLVE.format(repo=repo, rev=rev, path=urllib.parse.quote(entry["path"]))
    tmp = path + ".meas-download"
    for k in range(TRIES):
        try:
            h = hashlib.sha256() if lfs else hashlib.sha1(b"blob %d\0" % size)
            n = 0
            with get(url) as r, open(tmp, "wb") as f:
                while True:
                    b = r.read(CHUNK)
                    if not b:
                        break
                    f.write(b)
                    h.update(b)
                    n += len(b)
            if n == size and h.hexdigest() == want:
                os.replace(tmp, path)
                return rel, size, kind, want, "ok"
            outcome = f"mismatch size {n} hash {h.hexdigest()}"
        except Exception as e:   # retried; the last failure is recorded
            outcome = f"error {type(e).__name__}: {e}"
        time.sleep(5 * (k + 1))
    try:
        os.remove(tmp)
    except OSError:
        pass
    return rel, size, kind, want, outcome


def main():
    repo, rev, tree, dest, out_tsv = sys.argv[1:6]
    t0 = time.time()
    entries = listing(repo, rev, tree)
    files = [e for e in entries if e.get("type") == "file"]
    dirs = [e for e in entries if e.get("type") == "directory"]
    os.makedirs(dest, exist_ok=True)
    for d in dirs:
        os.makedirs(os.path.join(dest, d["path"][len(tree):].lstrip("/")), exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(THREADS) as ex:
        rows = list(ex.map(lambda e: fetch(repo, rev, e, tree, dest), files))
    with open(out_tsv, "w") as f:
        f.write("path\tsize\thash_kind\thash\toutcome\n")
        for r in sorted(rows):
            f.write("\t".join(str(x) for x in r) + "\n")
    ok = [r for r in rows if r[4] == "ok"]
    print(f"files={len(files)}")
    print(f"bytes={sum(e['size'] for e in files)}")
    print(f"directories={len(dirs)}")
    print(f"verified={len(ok)}")
    print(f"failed={len(rows) - len(ok)}")
    print(f"fetch_s={round(time.time() - t0)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
