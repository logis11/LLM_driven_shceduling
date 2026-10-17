import pathlib, sys, collections
sys.path.insert(0,'.'); import analyze_head as A
for rd in sorted(pathlib.Path('cli3').iterdir()):
    ph = A.load_phases(rd); w = A.good(ph, "tracker-daemon")
    series = {}
    for rec in A.iter_samples(rd):
        t = A.hms_us(rec["t"])
        if not A.in_phase(t, w): continue
        for p in rec["procs"]:
            if not p["comm"].startswith(("tracker","localsearch","dbus")): continue
            k=(p["pid"],p["starttime"])
            e=series.setdefault(k, {"comm":p["comm"],"t0":rec["t"],"c0":p["utime"]+p["stime"],"v0":p["vctxt"],"thr":0,"n":0})
            e.update(t1=rec["t"], c1=p["utime"]+p["stime"], v1=p["vctxt"]); e["thr"]=max(e["thr"],p["threads"]); e["n"]+=1
            e.setdefault("cfirst_abs", p["utime"]+p["stime"])
    print(rd.name, "window wall s", w[2]/1e6)
    for k,e in series.items():
        print(f"   {e['comm']:16s} pid={k[0]} thr={e['thr']} samples={e['n']} span={(e['t1']-e['t0'])/1e6:.1f}s ticks_in_window={e['c1']-e['c0']} ticks_at_first_sample={e['cfirst_abs']} vctxt={e['v1']-e['v0']}")
    # lifecycle: tracker execs/exits in window
    for line in (rd/'lifecycle.log').open(errors='replace'):
        if 'tracker' in line and (' exec ' in line or ' exit ' in line):
            ts = A.hms_str(line[:8])
            if w[0] <= ts <= w[1]+2: print("     LC:", line.rstrip()[:160])
