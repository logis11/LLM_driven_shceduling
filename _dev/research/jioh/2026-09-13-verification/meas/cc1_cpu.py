import pathlib, sys, collections, math, statistics
sys.path.insert(0,'.'); import analyze_head as A
for rd in sorted(pathlib.Path('cli3').iterdir()):
    ph = A.load_phases(rd)
    for bp in ("kernel-build-j8","kernel-build-cold"):
        w = A.good(ph, bp)
        first, last, comm = {}, {}, {}
        states = collections.Counter(); obs = 0
        live_cc1_peak = 0
        for rec in A.iter_samples(rd):
            t = A.hms_us(rec["t"])
            if not A.in_phase(t, w): continue
            n_cc1 = 0
            for p in rec["procs"]:
                if p["comm"] not in A.COMPILER_NAMES: continue
                k=(p["pid"],p["starttime"]); tk=p["utime"]+p["stime"]
                first.setdefault(k,tk); last[k]=tk; comm[k]=p["comm"]
                states[p["state"]] += 1; obs += 1
                if p["comm"]=="cc1": n_cc1 += 1
            live_cc1_peak = max(live_cc1_peak, n_cc1)
        ticks = collections.Counter(); seen = collections.Counter()
        for k in last:
            ticks[comm[k]] += last[k]-first[k]; seen[comm[k]] += 1
        # exit counts per name (birth in window)
        exits = collections.Counter()
        for line in (rd/"lifecycle.log").open(errors="replace"):
            m = A._EXIT.match(line)
            if not m: continue
            t, pid, dur, cmd = m.groups()
            b = pathlib.PurePath(cmd.split()[0]).name if cmd else ""
            if b not in A.COMPILER_NAMES: continue
            d = A.parse_duration_us(dur)
            if d is None: continue
            if w[0] <= A.hms_str(t)-d/1e6 <= w[1]: exits[b]+=1
        tot_ticks = sum(ticks.values())
        print(rd.name, bp, "total compiler cpu s", tot_ticks/100, "wall s", round(w[2]/1e6,1), "cpu/(4*wall)", round(tot_ticks/100/(4*w[2]/1e6),3), "peak cc1 live", live_cc1_peak)
        print("   share by comm:", {c: f"{ticks[c]/tot_ticks:.3f}" for c in ticks.most_common()})
        print("   cc1: cpu s", ticks['cc1']/100, "exits", exits['cc1'], "mean cpu/cc1 exit us", round(ticks['cc1']*1e4/exits['cc1']), "| per-TU (gcc exits)", exits['gcc'], "cpu/TU us", round(tot_ticks*1e4/exits['gcc']))
        print("   states of compiler-family observations:", dict(states), "D frac", round(states['D']/obs,4))
