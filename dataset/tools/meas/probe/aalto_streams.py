#!/usr/bin/env python3
"""Build the 136M Keystrokes stimulus streams for the stimulus-sensitivity
check (9.5 follow-ups spec, decision 11): per-repeat key streams in the
same shape as build_windows.py's SWELL-KW windows, replayed by the campaign's
`driven-alt` phase for the four typing-driven applications.

aalto_streams.py <cache-dir> <out-dir> [--zip PATH | --url URL] [--repeats 5]
                 [--window-s 600] [--seed 20260916] [--boundary-ms 2000]

Source: Dhakal, Feit, Kristensson, Oulasvirta, "Observations on Typing from
136 Million Keystrokes", CHI 2018 (`dhakal-chi18`); data
https://userinterfaces.aalto.fi/136Mkeystrokes/data/Keystrokes.zip (1.57 GB;
"free to use for research and non-commercial use with attribution",
readme.txt line 21). The zip is read by HTTP range requests: the ZIP64 end
records and central directory, then only the metadata file and the chosen
participant files (S3 search log, item 13), so nothing else is downloaded;
every fetched file is cached under <cache-dir> with its SHA-256 recorded.

Selection (design): participants from metadata_participants.txt with
KEYBOARD_TYPE in {full, laptop} and LAYOUT qwerty, shuffled with --seed;
taken in that order until each repeat holds --window-s seconds of recorded
time. Events are key presses (PRESS_TIME, ms); within a participant the
recorded gaps are kept, including the pauses between the 15 sentences
(reading the next stimulus); a participant boundary counts as one
--boundary-ms gap, as a file boundary does in the SWELL-KW windows. Keys
are not exported (D4). Output: <out-dir>/aalto-r<r>.jsonl and
<out-dir>/aalto-windows.json (participants, counts, spans, checksums).
"""

import argparse
import hashlib
import io
import json
import os
import random
import struct
import sys
import urllib.request
import zlib

URL = "https://userinterfaces.aalto.fi/136Mkeystrokes/data/Keystrokes.zip"


class RangeReader:
    """Byte-range access to a local file or an HTTP resource with Accept-Ranges."""

    def __init__(self, path=None, url=None):
        self.path, self.url = path, url
        if path:
            self.size = os.path.getsize(path)
        else:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req) as r:
                self.size = int(r.headers["Content-Length"])
                self.etag = r.headers.get("ETag"); self.last_modified = r.headers.get("Last-Modified")
                if r.headers.get("Accept-Ranges") != "bytes":
                    raise RuntimeError("server does not accept byte ranges")

    def read(self, start, length):
        if self.path:
            with open(self.path, "rb") as f:
                f.seek(start); return f.read(length)
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{start + length - 1}"})
        with urllib.request.urlopen(req) as r:
            if r.status != 206:
                raise RuntimeError(f"range request answered {r.status}")
            return r.read()


def central_directory(rr):
    """Parse the (ZIP64) end records and return {name: (local_header_offset, csize, usize, method)}."""
    tail = rr.read(rr.size - 1024, 1024)
    i = tail.rfind(b"PK\x05\x06")
    if i < 0:
        raise RuntimeError("no end-of-central-directory record")
    cd_size, cd_off = struct.unpack("<II", tail[i + 12:i + 20])
    j = tail.rfind(b"PK\x06\x07", 0, i)
    if j >= 0:  # a ZIP64 locator is present (this archive has more than 65 535 members): the ZIP64 record is authoritative
        z64_off = struct.unpack("<Q", tail[j + 8:j + 16])[0]
        rec = rr.read(z64_off, 56)
        if rec[:4] != b"PK\x06\x06":
            raise RuntimeError("bad ZIP64 end record")
        cd_size, cd_off = struct.unpack("<QQ", rec[40:56])
    cd = rr.read(cd_off, cd_size)
    entries = {}
    p = 0
    while p + 46 <= len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        method, = struct.unpack("<H", cd[p + 10:p + 12])
        csize, usize = struct.unpack("<II", cd[p + 20:p + 28])
        n, m, k = struct.unpack("<HHH", cd[p + 28:p + 34])
        off, = struct.unpack("<I", cd[p + 42:p + 46])
        name = cd[p + 46:p + 46 + n].decode("utf-8", "replace")
        extra = cd[p + 46 + n:p + 46 + n + m]
        q = 0
        while q + 4 <= len(extra):
            hid, hlen = struct.unpack("<HH", extra[q:q + 4])
            if hid == 0x0001:
                body = extra[q + 4:q + 4 + hlen]; b = 0
                if usize == 0xFFFFFFFF:
                    usize, = struct.unpack("<Q", body[b:b + 8]); b += 8
                if csize == 0xFFFFFFFF:
                    csize, = struct.unpack("<Q", body[b:b + 8]); b += 8
                if off == 0xFFFFFFFF:
                    off, = struct.unpack("<Q", body[b:b + 8]); b += 8
            q += 4 + hlen
        entries[name] = (off, csize, usize, method)
        p += 46 + n + m + k
    return entries


def fetch_member(rr, entry, cache_path):
    """Inflate one member (via its local header) into cache_path; return its SHA-256."""
    if os.path.exists(cache_path):
        return hashlib.sha256(open(cache_path, "rb").read()).hexdigest()
    off, csize, usize, method = entry
    lh = rr.read(off, 30)
    if lh[:4] != b"PK\x03\x04":
        raise RuntimeError("bad local header")
    n, m = struct.unpack("<HH", lh[26:30])
    data = rr.read(off + 30 + n + m, csize)
    raw = zlib.decompress(data, -15) if method == 8 else data
    if len(raw) != usize:
        raise RuntimeError(f"inflated {len(raw)} bytes, expected {usize}")
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    open(cache_path, "wb").write(raw)
    return hashlib.sha256(raw).hexdigest()


def presses(path):
    """Sorted (press_ms, section) of one participant file; sections in order of first press."""
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8", errors="replace")]
    h = rows[0]
    try:
        i_sec, i_press = h.index("TEST_SECTION_ID"), h.index("PRESS_TIME")
    except ValueError:
        return []
    out = []
    for r in rows[1:]:
        if len(r) != len(h):
            continue
        try:
            out.append((int(r[i_press]), r[i_sec]))
        except ValueError:
            continue
    out.sort()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cache"); ap.add_argument("out")
    ap.add_argument("--zip", default=None); ap.add_argument("--url", default=URL)
    ap.add_argument("--repeats", type=int, default=5); ap.add_argument("--window-s", type=float, default=600.0)
    ap.add_argument("--seed", type=int, default=20260916); ap.add_argument("--boundary-ms", type=float, default=2000.0)
    a = ap.parse_args()
    rr = RangeReader(path=a.zip, url=None if a.zip else a.url)
    print(f"zip size {rr.size}", file=sys.stderr)
    cd_cache = os.path.join(a.cache, "central_directory.json")
    if os.path.exists(cd_cache):
        entries = {k: tuple(v) for k, v in json.load(open(cd_cache)).items()}
    else:
        entries = central_directory(rr)
        os.makedirs(a.cache, exist_ok=True); json.dump(entries, open(cd_cache, "w"))
    print(f"{len(entries)} members", file=sys.stderr)
    sums = {}
    for name in ("Keystrokes/files/readme.txt", "Keystrokes/files/metadata_participants.txt"):
        sums[name] = fetch_member(rr, entries[name], os.path.join(a.cache, os.path.basename(name)))
    meta = [l.rstrip("\n").split("\t") for l in open(os.path.join(a.cache, "metadata_participants.txt"), encoding="utf-8", errors="replace")]
    h = meta[0]
    i_id, i_kb, i_layout = h.index("PARTICIPANT_ID"), h.index("KEYBOARD_TYPE"), h.index("LAYOUT")
    pool = sorted(r[i_id] for r in meta[1:] if len(r) == len(h) and r[i_kb] in ("full", "laptop") and r[i_layout].lower() == "qwerty")
    print(f"pool {len(pool)} participants (full/laptop, qwerty)", file=sys.stderr)
    rng = random.Random(a.seed)
    rng.shuffle(pool)
    os.makedirs(a.out, exist_ok=True)
    index = {}
    k = 0
    for r in range(1, a.repeats + 1):
        win = []  # (gap_ms, participant)
        span = 0.0
        used = []
        while span < a.window_s and k < len(pool):
            pid = pool[k]; k += 1
            name = f"Keystrokes/files/{pid}_keystrokes.txt"
            if name not in entries:
                continue
            path = os.path.join(a.cache, f"{pid}_keystrokes.txt")
            sums[name] = fetch_member(rr, entries[name], path)
            ev = presses(path)
            if len(ev) < 50:
                continue
            used.append(pid)
            prev = None
            for t, _ in ev:
                if prev is None:
                    gap = a.boundary_ms if win else 0.0
                else:
                    gap = max(0.0, float(t - prev))
                win.append((gap, pid)); span += gap / 1000.0; prev = t
                if span >= a.window_s:
                    break
        with open(os.path.join(a.out, f"aalto-r{r}.jsonl"), "w") as f:
            for gap, _ in win:
                f.write(json.dumps({"gap_ms": round(gap, 1), "seg": 0, "kind": "key", "x": None, "y": None,
                                    "button": None, "wheel": None}) + "\n")
        gaps = sorted(g for g, _ in win[1:])
        q = lambda p: round(gaps[min(len(gaps) - 1, int(p * (len(gaps) - 1)))], 1) if gaps else None
        index[f"aalto-r{r}"] = {"participants": used, "events": len(win), "keys": len(win), "pointer": 0,
                                "span_s": round(span, 1), "gap_ms_p50": q(.5), "gap_ms_p90": q(.9), "gap_ms_p99": q(.99),
                                "share_gt_1s": round(sum(g > 1000 for g in gaps) / max(len(gaps), 1), 4)}
        print(f"aalto-r{r}: {len(used)} participants, {len(win)} keys, {span:.1f} s, gap p50 {q(.5)} p90 {q(.9)}", file=sys.stderr)
    json.dump({"rule": f"spec decision 11: participants with KEYBOARD_TYPE full/laptop and LAYOUT qwerty, shuffled with seed {a.seed}, "
                       f"taken in order until {a.window_s:.0f} s per repeat; recorded gaps kept within a participant (sentence pauses included); "
                       f"{a.boundary_ms:.0f} ms per participant boundary; keys not exported (D4)",
               "dataset": "136M Keystrokes (dhakal-chi18), " + a.url, "zip_size": rr.size,
               "zip_etag": getattr(rr, "etag", None), "zip_last_modified": getattr(rr, "last_modified", None),
               "pool": len(pool), "sha256": sums, "windows": index},
              open(os.path.join(a.out, "aalto-windows.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
