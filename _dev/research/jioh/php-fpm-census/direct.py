#!/usr/bin/env python3
"""Of each component's outside-cause wakes, how many the outside cause raised itself and how many inherit it through
the chain rule. A wake is `direct` when its own wakeup row — the last row to the thread at or before its schedule-in
— names an outside waker (by census_core's classes; a born-in-phase process by its ancestry); otherwise it is outside
only because a tree thread woke it while running in a wake whose cause is outside (D27 decision 2), or because it
continues such a wake after a block in D.

  python3 -I direct.py <census.json> <out.json> <root> [<root> ...]

<root>: the extracted release folders the census read (campaign and desktop families), or, for a background section,
the folder holding `meas-background-<job>-r<k>-full.zip` (its wakeups file is read from the zip).
"""

import bisect
import collections
import glob
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402

NAME = re.compile(r"^meas-(interactive|playback|desktop)-(.+)-r(\d+)-(full|dry|idle)$")


def campaign_dirs(roots, app):
    out = {}
    for root in roots:
        for d in sorted(glob.glob(os.path.join(root, "**", "meas-*"), recursive=True)):
            m = NAME.match(os.path.basename(d))
            if m and m.group(2) == app and "-excluded" not in d and os.path.exists(os.path.join(d, "report.json")):
                out.setdefault(int(m.group(3)), []).append(d)
    return out


def direct_counts(wakeup_rows, gone):
    """gone: [[t_in, ..., tid at index 1 or 2, ...]] -> (direct, inherited, labels of the direct)."""
    to = collections.defaultdict(list)
    tids = {g[2] if isinstance(g[1], str) else g[1] for g in gone}
    for w in wakeup_rows:
        if w[5] in tids:
            to[w[5]].append(w)
    for v in to.values():
        v.sort(key=lambda w: w[0])
    times = {tid: [w[0] for w in v] for tid, v in to.items()}
    tr = cc.Tracer(wakeup_rows, set(), {})   # every row: a born process's ancestry is read from them
    d, inh, lab = 0, 0, collections.Counter()
    for g in gone:
        t, tid = g[0], (g[2] if isinstance(g[1], str) else g[1])
        rs = to.get(tid, [])
        j = bisect.bisect_right(times.get(tid, []), t + cc.EPS) - 1
        if j < 0 or rs[j][3] is None:
            inh += 1
            continue
        cls, l = tr.process(rs[j][3], rs[j][1])
        if cls == "outside":
            d += 1
            lab[f"{rs[j][1]} -> {l}"] += 1
        else:
            inh += 1
    return d, inh, lab


def main():
    census, out_path, roots = sys.argv[1], sys.argv[2], sys.argv[3:]
    data = json.load(open(census))
    result = {}
    for sec, e in data.items():
        phase = e["phase"]
        app = e.get("app")
        dirs = campaign_dirs(roots, app) if app else {}
        for k, res in e["repeats"].items():
            gone_all = [(comp, g) for comp, c in res.items() for g in c.get("gone", []) if "outside" in g]
            if not gone_all:
                continue
            if app:
                kk = int(k.split("@")[0])
                cands = dirs.get(kk, [])
                if "@" in k:
                    cands = [d for d in cands if k.split("@")[1] in d or k.split("@")[1] in open(
                        os.path.join(d, "spec.json")).read()]
                wk = os.path.join(cands[0], f"perf.{phase}.wakeups.txt.gz")
                rows = list(cc.iter_wakeup_rows(wk))
            else:
                job = "7z" if sec == "file-archiver" else "steamcmd"
                z = zipfile.ZipFile(os.path.join(roots[0], f"meas-background-{job}-r{k}-full.zip"))
                name = next(n for n in z.namelist() if n.endswith(f"perf.{phase}.wakeups.txt.gz"))
                tmp = os.path.join(os.path.dirname(out_path), f"_wk_{job}_{k}.txt.gz")
                with open(tmp, "wb") as fh:
                    fh.write(z.read(name))
                rows = list(cc.iter_wakeup_rows(tmp))
                os.remove(tmp)
            by_comp = collections.defaultdict(list)
            for comp, g in gone_all:
                by_comp[comp].append(g)
            for comp, gs in by_comp.items():
                d, inh, lab = direct_counts(rows, gs)
                r = result.setdefault(sec, {}).setdefault(comp, {"outside": 0, "direct": 0, "inherited": 0,
                                                                 "direct_by_waker": collections.Counter(),
                                                                 "direct_per_repeat": {}})
                r["outside"] += len(gs)
                r["direct"] += d
                r["inherited"] += inh
                r["direct_by_waker"].update(lab)
                r["direct_per_repeat"][k] = d
            print(f"{sec} r{k}: done", flush=True)
    for sec in result.values():
        for r in sec.values():
            r["direct_by_waker"] = dict(r["direct_by_waker"].most_common())
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
