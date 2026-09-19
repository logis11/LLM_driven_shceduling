#!/usr/bin/env python3
"""Watch a campaign: relaunch windows the machine gate stopped, stop on the first event that needs a decision.

watch.py <family>[/<app>]... [--since N] [--app APP:N]... [--done APP,...] [--poll S] [--from-now]

Every S seconds (default 30) the family's runs numbered N or later are read. N is the run of the latest launch — the
default, the family's newest run when the watcher starts — never the campaign's first run: reading every run of a long
campaign takes minutes a pass and leaves a gated window unrelaunched that long. --app APP:N gives one application its
own first run. A job that
finished in under common.GATE_S is read from its report: stopped by the machine gate, it is relaunched with the same
window or repeat index (9.5 D26) — only while its application has no other job in flight outside its first run (one
relaunch or added repeat at a time), and never for an application in --done. The watcher exits, printing the event, when
a watched job lands, fails, or ends short without the gate. Handled jobs are kept in <work>/watch-seen.txt, so a restart
does not repeat them; a completed run whose jobs are all handled is not read again. --from-now counts every job already
finished at the start as handled.
"""

import os
import sys
import time

import common


def main():
    a = sys.argv[1:]
    if not a:
        raise SystemExit(__doc__)
    targets, since, app_since, done, poll, from_now = [], None, {}, set(), 30, False
    i = 0
    while i < len(a):
        if a[i] == "--since":
            since = int(a[i + 1]); i += 2
        elif a[i] == "--app":
            n, _, s = a[i + 1].partition(":"); app_since[n] = int(s); i += 2
        elif a[i] == "--done":
            done |= set(a[i + 1].split(",")); i += 2
        elif a[i] == "--poll":
            poll = int(a[i + 1]); i += 2
        elif a[i] == "--from-now":
            from_now = True; i += 1
        else:
            targets.append(common.parse_target(a[i])[:2]); i += 1
    if since is None:   # the newest run of the watched families: the latest launch
        since = min(common.runs(fam)[-1]["number"] for fam in {f for f, _ in targets})
    print(f"watching runs from #{since}", flush=True)
    os.makedirs(common.WORK, exist_ok=True)
    seen_path = os.path.join(common.WORK, "watch-seen.txt")
    seen = set(open(seen_path).read().split("\n")) if os.path.exists(seen_path) else set()
    closed, deferred = set(), set()
    if from_now:
        for fam in sorted({f for f, _ in targets}):
            for r in common.runs(fam, since):
                for j in common.jobs(fam, r["databaseId"]):
                    if j["state"] not in ("queued", "measuring"):
                        seen.add(f"{r['databaseId']}:{j['name']}")
        open(seen_path, "w").write("\n".join(sorted(seen)) + "\n")
    watched = lambda f, app: (f, None) in targets or (f, app) in targets
    first = lambda app: app_since.get(app, since)
    while True:
        events, gated, busy = [], [], set()
        for fam in sorted({f for f, _ in targets}):
            for r in common.runs(fam, since):
                if r["databaseId"] in closed:
                    continue
                js = [j for j in common.jobs(fam, r["databaseId"]) if watched(fam, j["app"]) and r["number"] >= first(j["app"])]
                for j in js:
                    key = f"{r['databaseId']}:{j['name']}"
                    if j["state"] in ("queued", "measuring"):
                        if r["number"] != first(j["app"]):
                            busy.add((fam, j["app"]))
                        continue
                    if key in seen:
                        continue
                    if j["state"] == "landed":
                        events.append(f"LANDED {fam} {j['name']} run {r['databaseId']} ({j['seconds']:.0f} s)")
                    elif j["state"] == "failed":
                        events.append(f"FAILED {fam} {j['name']} run {r['databaseId']}")
                    else:
                        gate, model = common.gate_of(fam, j)
                        if gate == "wrong-machine":   # handled once relaunched: one left for later is read again
                            gated.append((fam, j["app"], j["k"], model, key))
                            continue
                        events.append(f"SHORT without the gate {fam} {j['name']} run {r['databaseId']}: gate {gate}")
                    seen.add(key); open(seen_path, "a").write(key + "\n")
                if r["status"] == "completed" and all(f"{r['databaseId']}:{j['name']}" in seen for j in js):
                    closed.add(r["databaseId"])
        go = []
        for fam, app, k, model, key in gated:
            if app in done:
                seen.add(key); open(seen_path, "a").write(key + "\n")
                print(f"{time.strftime('%H:%M')} {app} r{k} gated ({model}); not relaunched ({app} done)", flush=True)
                continue
            if (fam, app) in busy or any(x[:2] == (fam, app) for x in go):
                if key not in deferred:
                    deferred.add(key)
                    print(f"{time.strftime('%H:%M')} {app or 'build'} r{k} gated ({model}); left for the next check", flush=True)
                continue
            go.append((fam, app, k, key))
            print(f"{time.strftime('%H:%M')} {app or 'build'} r{k} gated ({model}); relaunched", flush=True)
        if go:
            print("   " + common.push_trigger([x[:3] for x in go], "retried"), flush=True)
            for x in go:   # handled only once the relaunch is pushed
                seen.add(x[3]); open(seen_path, "a").write(x[3] + "\n")
        if events:
            print("\n".join(events)); return
        time.sleep(poll)


if __name__ == "__main__":
    main()
