#!/usr/bin/env python3
"""The `podman` job's wakes of Kdenlive's idle main thread (9.10, `meas-ci:interactive:2026-10-05`, `video-editor` idle
phase): every wakeup row a `podman` process raises outside its own process, grouped into bursts (one waker thread, rows
within 50 µs), with the processes each burst wakes, the expedited-RCU kernel thread's rows after it, and Kdenlive's
D-Bus thread's wakes of its main thread in the 5 ms after it — read from each repeat's wakeup rows.

  python3 -I podman_wakes.py <out.json> <repeat dir> [<repeat dir> ...]
"""

import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import census_core as cc  # noqa: E402

DIRNAME = re.compile(r"-r(\d+)-idle")


def one(D):
    rows = list(cc.iter_wakeup_rows(os.path.join(D, "perf.idle.wakeups.txt.gz")))
    rows.sort(key=lambda w: w[0])
    snap = json.load(open(os.path.join(D, "snap.idle.before.json")))
    app = {p["pid"] for p in snap["procs"] if p.get("comm") == "kdenlive"}
    podman = {w[3] for w in rows if w[1] in ("podman", "(podman)")} | {w[6] for w in rows if w[4] == "(podman)"}
    starts = [(round(w[0], 6), w[6]) for w in rows if w[4] == "(podman)" and w[1] == "systemd" and w[3] == 1]
    out_rows = [w for w in rows if w[3] in podman and w[6] not in podman and not cc.KTHREAD.search(w[4] or "")]
    bursts = []
    for w in out_rows:
        if bursts and w[2] == bursts[-1]["waker_tid"] and w[0] - bursts[-1]["last"] <= 50e-6:
            b = bursts[-1]
        else:
            b = {"t": round(w[0], 6), "waker": f"{w[1]}[{w[2]}/{w[3]}]", "waker_tid": w[2], "woken": [], "last": w[0]}
            bursts.append(b)
        b["woken"].append(f"{w[4]}[{w[5]}/{w[6]}]")
        b["last"] = w[0]
    for b in bursts:
        t = b.pop("last")
        b.pop("waker_tid")
        b["rcu_exp_after_ms"] = [round((w[0] - b["t"]) * 1000, 3) for w in rows
                                 if b["t"] <= w[0] <= t + 0.003 and w[4].startswith("rcu_exp")]
        b["app_dbus_after_ms"] = [round((w[0] - b["t"]) * 1000, 3) for w in rows
                                  if b["t"] < w[0] <= t + 0.005 and w[1] == "QDBusConnection" and w[3] in app
                                  and w[6] in app and w[5] in app]
        b["udisksd_dbus_after_ms"] = [round((w[0] - b["t"]) * 1000, 3) for w in rows
                                      if b["t"] < w[0] <= t + 0.005 and w[1] == "udisksd" and w[4] == "gdbus"]
    return {"dir": D, "app_pids": sorted(app), "podman_unit_starts": starts, "bursts": bursts,
            "app_woken": sum(1 for b in bursts for x in b["woken"] if int(x.split("/")[-1].rstrip("]")) in app)}


def main():
    out_path, dirs = sys.argv[1], sys.argv[2:]
    result = {}
    for D in dirs:
        k = DIRNAME.search(os.path.basename(D)).group(1)
        r = one(D)
        result[k] = r
        print(f"r{k}: podman unit starts {len(r['podman_unit_starts'])}, bursts {len(r['bursts'])}, Kdenlive woken "
              f"{r['app_woken']}", flush=True)
        for b in r["bursts"]:
            print(f"   {b['t']} {b['waker']}: {' '.join(b['woken'])}; rcu_exp +{b['rcu_exp_after_ms']} ms; "
                  f"udisksd D-Bus +{b['udisksd_dbus_after_ms']}; Kdenlive's D-Bus thread to its main +{b['app_dbus_after_ms']}",
                  flush=True)
    json.dump(result, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
