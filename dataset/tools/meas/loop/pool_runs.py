#!/usr/bin/env python3
"""Pool one application's landed repeats across a campaign's runs, check each repeat's validity, report the stability rule.

pool_runs.py <family>/<app> [--since N] [--out FILE] [--exclude K[,K]... --exclude-why TEXT] [-- <pool.py options>]
pool_runs.py build [--since N] [--out FILE] [--exclude K[,K]... --exclude-why TEXT] [-- <pool.py options>]
pool_runs.py background/<app> [--since N] [--out FILE] [--exclude K[,K]... --exclude-why TEXT] [-- <pool.py options>]

Every landed artifact (common.GATE_S or longer, success) of runs numbered N or later is downloaded under the work
directory — one folder per run for families with apps, one flat folder for build (its repeat indices never repeat) —
and pooled with the family's pool.py and --cpu-model common.MACHINE. Options after -- go to pool.py (chrome:
--exclude-roles renderer, 9.5 D14). Validity per repeat (_dev/research/jioh/measurement-campaign-workflow.md, the loop,
step 4): gate open on the machine; the replay sent every event of its window; operations completed; non-zero return
codes other than perf record's 130 (its SIGINT stop) and freshclam's 2 with a recorded database; for build, one
ClamAV signature database across the repeats whose clamscan is pooled (9.6 D27); for background, the set's archive and manifest matching their pins and the
tree verified after each change set, every SteamCMD phase reporting its install complete, one app build across repeats.

--exclude leaves a repeat out of the pool, --exclude-why states why in the printed lines and in the pooled record
(`excluded_repeats`); a repeat the validity step fails counts for nothing (workflow guide, the loop, step 4), and the
rule, the projection and every value are then read over the rest. The artifact is moved to <pool folder>-excluded, out
of the folder pool.py reads, and is not downloaded again.
"""

import json
import os
import subprocess
import sys

import common


def kv(path):
    try:
        return dict(line.rstrip("\n").split("=", 1) for line in open(path) if "=" in line)
    except OSError:
        return {}


def lines(path):
    try:
        return sum(1 for _ in open(path))
    except OSError:
        return None


def validity(family, dirs, entry):
    """One line per repeat; returns the number of repeats with a problem."""
    streams = os.path.join(common.REPO, "dataset/meas/streams")
    win = json.load(open(os.path.join(streams, "windows.json")))["windows"] if os.path.exists(os.path.join(streams, "windows.json")) else {}
    alt = json.load(open(os.path.join(streams, "aalto-windows.json")))["windows"] if os.path.exists(os.path.join(streams, "aalto-windows.json")) else {}
    bad, dbs = 0, set()
    op = (entry or {}).get("phases", {}).get("op", {}).get("operation")
    reps = (entry or {}).get("phases", {}).get("op", {}).get("repeats") or (entry or {}).get("repeats", [])
    # every phase present (the loop, step 4): a repeat past the recording's end runs the idle phase alone (9.5 D32);
    # any other repeat has every phase some repeat of the application has
    has = {k: {f.split(".")[1] for f in os.listdir(d) if f.startswith("perf.") and ".timehist.txt" in f} for k, d in dirs.items()}
    full = set().union(*has.values()) if has else set()
    for k, d in sorted(dirs.items()):
        rep, r = json.load(open(os.path.join(d, "report.json"))), kv(os.path.join(d, "report.kv"))
        notes, info = [], []
        if r.get("recording.past_end") == "1":
            info.append("idle phase only, past the recording's end (9.5 D32)")
        elif family in ("interactive", "playback") and has[k] != full:
            notes.append(f"phases missing {sorted(full - has[k])}")
        if r.get("recording.window") == "uncut":
            notes.append("input window not cut")
        if rep.get("gate") != "open" or common.MACHINE not in (rep.get("machine.model") or ""):
            notes.append(f"gate {rep.get('gate')} on {rep.get('machine.model')}")
        # explained: perf record's 130 is its SIGINT stop; freshclam's 2 is the system service holding the update lock,
        # harmless when the scan's signature database was recorded (and is compared across repeats below)
        rcs = {x: v for x, v in r.items() if x.endswith(".rc") and v not in ("0", "")
               and not (x.startswith("perf.") and x.endswith(".record.rc") and v == "130")
               and not (x == "freshclam.rc" and v == "2" and r.get("clamav.db"))}
        if rcs:
            notes.append(f"rc {rcs}")
        if r.get("stream_file"):
            w = win.get(r["stream_file"].removesuffix(".jsonl"), {})
            want = w.get("keys") if r.get("stream_kinds") == "key" else w.get("events")
            sent = lines(os.path.join(d, "replay.jsonl"))
            if want is not None and sent is not None and sent < want:
                notes.append(f"replay sent {sent} of {want}")
        if r.get("stream_alt_file"):
            want, sent = alt.get(r["stream_alt_file"].removesuffix(".jsonl"), {}).get("keys"), lines(os.path.join(d, "replay-alt.jsonl"))
            if want is not None and sent is not None and sent < want - 2:   # a 136M window may run a key past 600 s
                notes.append(f"driven-alt sent {sent} of {want}")
        if op and k in reps and op["n_failed"][reps.index(k)]:
            notes.append(f"operations failed {op['n_failed'][reps.index(k)]} of {op['n_ok'][reps.index(k)] + op['n_failed'][reps.index(k)]}")
        if family == "build":   # 9.6 D27: the repeats whose clamscan is pooled read one signature database
            if k in (entry or {}).get("phases", {}).get("clamscan", {}).get("repeats", []):
                dbs.add((entry or {}).get("clamav_daily", {}).get(str(k)) or (entry or {}).get("clamav_daily", {}).get(k))
        elif r.get("clamav.db"):
            dbs.add(r["clamav.db"])
        if family == "background":
            pins = {x: v for x, v in r.items() if x.startswith("set.") and x.endswith("_pin") and v != "ok"}
            if pins:
                notes.append(f"set pins {pins}")
            bad_verify = {x: v for x, v in r.items() if x.startswith("set.verify.") and v != "ok"}
            if bad_verify:
                notes.append(f"set not restored {bad_verify}")
            incomplete = [x for x, v in r.items() if x.startswith("steam.") and x.endswith(".success") and v != "1"]
            if incomplete:
                notes.append(f"SteamCMD install not reported complete {incomplete}")
            if r.get("steam.buildid"):
                dbs.add(r["steam.buildid"])
        bad += bool(notes)
        print(f"   r{k}: {'ok' if not notes else '; '.join(notes)}{''.join(f' ({x})' for x in info)}")
    if len(dbs) > 1:
        what = "SteamCMD app builds" if family == "background" else "ClamAV signature databases"
        print(f"   {what} differ across repeats: {sorted(dbs)}"); bad += 1
    return bad


def main():
    a = sys.argv[1:]
    passthrough = a[a.index("--") + 1:] if "--" in a else []
    a = a[:a.index("--")] if "--" in a else a
    if not a:
        raise SystemExit(__doc__)
    family, app, _ = common.parse_target(a[0])
    since = int(a[a.index("--since") + 1]) if "--since" in a else 1
    base = os.path.join(common.WORK, "pool", f"{family}-{app or 'build'}-from{since}")
    out = a[a.index("--out") + 1] if "--out" in a else os.path.join(base, "pooled.json")
    excluded = {int(k) for k in a[a.index("--exclude") + 1].split(",")} if "--exclude" in a else set()
    why = a[a.index("--exclude-why") + 1] if "--exclude-why" in a else ""
    if excluded and not why:
        raise SystemExit('--exclude needs --exclude-why "<reason>": the pooled record states why a repeat is left out')
    dirs = {}
    for r in common.runs(family, since):
        names = None
        for j in common.jobs(family, r["databaseId"]):
            if j["state"] != "landed" or (app and j["app"] != app):
                continue
            name = common.artifact(family, j["app"], j["k"])
            names = common.artifact_names(r["databaseId"]) if names is None else names
            if name not in names:   # a dry check or another mode: not a repeat of this campaign
                print(f"   run #{r['number']} ({r['databaseId']}): no {name} (has {', '.join(names) or 'none'}); not pooled")
                continue
            dest = os.path.join(base, name) if family == "build" else os.path.join(base, str(r["databaseId"]), name)
            if j["k"] in excluded:   # out of the folder pool.py reads, kept beside it, never downloaded again
                aside = os.path.join(base + "-excluded", str(r["databaseId"]), name)
                if os.path.exists(dest) and not os.path.exists(aside):
                    os.makedirs(os.path.dirname(aside), exist_ok=True)
                    os.replace(dest, aside)
                print(f"   r{j['k']}: left out of the pool — {why}; its artifact under {base}-excluded")
                continue
            dirs[j["k"]] = common.download(r["databaseId"], name, dest)
    if not dirs:
        raise SystemExit("no landed repeat")
    cmd = ["python3", common.FAMILIES[family]["pool"], base, out, "--cpu-model", common.MACHINE, *passthrough]
    if family in ("build", "background") and "--md" not in passthrough:
        cmd += ["--md", os.path.join(os.path.dirname(out), "results.md")]
    p = subprocess.run(cmd, cwd=common.REPO, capture_output=True, text=True)
    if p.returncode:
        raise SystemExit(p.stderr[-3000:])
    pooled = json.load(open(out))
    entry = pooled if family == "build" else pooled["runs"].get(app)
    st = (entry or {}).get("stability")
    if excluded:
        (entry if entry is not None else pooled)["excluded_repeats"] = {str(k): why for k in sorted(excluded)}
        json.dump(pooled, open(out, "w"), indent=1)
        md = next((cmd[i + 1] for i, a in enumerate(cmd) if a == "--md"), None)   # the pool rendered before this key existed
        if md and os.path.exists(md):
            with open(md, "a") as handle:
                handle.write(f"\n## Left out of this pool\n\nRepeat(s) {', '.join(str(k) for k in sorted(excluded))}: {why}\n")
    if family == "build":
        crit = st["quantities"]
        print(f"build: repeats {pooled['repeats']}; stability rule {'holds' if st['passes'] else 'does not hold yet'}; "
              f"repeats needed at this spread {st.get('needed') or 'over 200'}"
              + (f"; not estimable yet: {', '.join(st['not_estimable'])}" if st.get("not_estimable") else ""))
        for ph, P in pooled["phases"].items():
            if P.get("not_pooled"):
                print(f"   {ph} pooled over {P.get('repeats', [])}; not pooled: {({r: x['why'] for r, x in P['not_pooled'].items()})} (9.6 D27, D28)")
        for q, c in crit.items():
            print(f"   {q}: k {c['k']}, mean {c['mean']}, half-width {c['half_width']} (abs {c['half_width_abs']}), "
                  f"needed {c.get('needed')}, "
                  + ("carried with its half-width (9.6 D29)" if c.get("excepted") and c.get("carried")
                     else ("passes" if c["passes"] else "fails")))
    elif st and "quantities" in st:
        print(f"{app}: repeats {entry['repeats']}; stability rule {'holds' if st['passes'] else 'does not hold yet'}"
              + (f"; first batch at this spread {entry['first_batch']['count']}" if entry.get("first_batch") else ""))
        for q, c in st["quantities"].items():
            print(f"   {q}: k {c['k']}, half-width {c['half_width']}, "
                  f"{'passes' if c['passes'] else 'at the window limit, reported (D46)' if c.get('limited') else 'fails'}")
    elif st:
        print(f"{app}: repeats {entry['repeats']}; {st['quantity']} over {st['k']}: half-width {st['half_width']} "
              f"(tolerance {st['tolerance']}) — {'holds' if st['passes'] else 'does not hold yet'}")
        print(f"   values {st['values']}")
    print(f"   phases {list((entry or {}).get('phases', {}))}; pooled record {out}")
    print("validity:")
    bad = validity(family, dirs, entry)
    if excluded:
        print(f"   left out of this pool: {sorted(excluded)} — {why}")
    print(f"   {'every repeat valid' if not bad else f'{bad} repeat(s) with a problem'}")


if __name__ == "__main__":
    main()
