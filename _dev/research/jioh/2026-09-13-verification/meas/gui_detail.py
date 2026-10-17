import json, pathlib, sys, collections
sys.path.insert(0,'.')
import analyze_head as A
base = pathlib.Path('gui')
for rd in sorted(base.iterdir()):
    ph = A.load_phases(rd)
    for phase, match in (("chromium-10-tabs", lambda c: c.startswith(("chrom","chrome"))), ("element-idle", lambda c: c.lower().startswith("element")), ("element-idle", lambda c: c in A.DAEMON_NAMES)):
        w = ph[phase]
        series = {}
        nsamp = 0; comms = collections.Counter(); ts=[]
        for rec in A.iter_samples(rd):
            t = A.hms_us(rec["t"])
            if not A.in_phase(t, w): continue
            nsamp += 1; ts.append(rec["t"])
            for p in rec["procs"]:
                if not match(p["comm"]): continue
                key=(p["pid"],p["starttime"])
                e = series.setdefault(key, {"comm":p["comm"],"t0":t,"v0":p["vctxt"],"c0":p["utime"]+p["stime"],"thr":0,"nv0":p["nvctxt"]})
                e.update(t1=t, v1=p["vctxt"], c1=p["utime"]+p["stime"], nv1=p["nvctxt"]); e["thr"]=max(e["thr"],p["threads"])
        gaps = [(b-a)/1000 for a,b in zip(ts,ts[1:])]
        gaps.sort()
        print(rd.name, phase, "samples", nsamp, "sample-interval ms median/p99/max", round(gaps[len(gaps)//2]), round(gaps[int(len(gaps)*.99)]), round(gaps[-1]), "procs seen", len(series))
        for k,e in sorted(series.items(), key=lambda kv: kv[1]["comm"]):
            span=e["t1"]-e["t0"]; wakes=e["v1"]-e["v0"]; ticks=e["c1"]-e["c0"]
            kept = span>=5 and wakes>=5
            if phase=="element-idle" and match("systemd") and not kept: continue
            print(f"   {e['comm']:18s} pid={k[0]:6d} thr={e['thr']:3d} span={span:4d}s wakes={wakes:6d} nvwakes={e['nv1']-e['nv0']:5d} ticks={ticks:5d} kept={kept} gap_ms={span*1e3/wakes if wakes else None} work_us={ticks*1e4/wakes if wakes else None}")
