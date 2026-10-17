import pathlib, sys, collections
sys.path.insert(0,'.'); import analyze_head as A
PH = [("rsync-copy",{"rsync"}),("untar",{"tar","xz"}),("clamscan",{"clamscan"}),("updatedb",{"updatedb.plocate","updatedb"}),("network-bulk",{"wget"}),("download-verify",{"wget","xz"}),("tar-read-cold",{"tar"}),("rsync-copy-cold",{"rsync"}),("clamscan-cold",{"clamscan"}),("updatedb-cold",{"updatedb.plocate","updatedb"})]
for rd in sorted(pathlib.Path('cli3').iterdir()):
    ph = A.load_phases(rd)
    samples = [(A.hms_us(r["t"]), r["t"], [p for p in r["procs"]]) for r in A.iter_samples(rd)]
    print(rd.name)
    for name, comms in PH:
        w = A.good(ph, name)
        if not w: print("  ", name, "no window"); continue
        n = 0; per = {}
        for t, tus, procs in samples:
            if not A.in_phase(t, w): continue
            n += 1
            for p in procs:
                if p["comm"] in comms:
                    k=(p["pid"],p["starttime"]); e=per.setdefault(k,[p["comm"],t,p["utime"]+p["stime"],t,0,p["threads"],0])
                    e[3]=t; e[4]=p["utime"]+p["stime"]; e[6]+=1
        rows = [f"{e[0]}:samples={e[6]},span={e[3]-e[1]}s,ticks={e[4]-e[2]},thr={e[5]}" for e in per.values()]
        print(f"   {name:16s} wall={w[2]/1e6:6.1f}s intwindow=[{w[0]},{w[1]}]({w[1]-w[0]}s) samples_in_window={n} procs: {rows}")
