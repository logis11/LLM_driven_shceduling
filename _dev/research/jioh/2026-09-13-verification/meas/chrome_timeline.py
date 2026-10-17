import json, pathlib, sys, collections
sys.path.insert(0,'.')
import analyze_head as A
for rd in sorted(pathlib.Path('gui').iterdir()):
    ph = A.load_phases(rd); w = ph["chromium-10-tabs"]
    start = None; counts = []
    for rec in A.iter_samples(rd):
        t = A.hms_us(rec["t"])
        if not A.in_phase(t, w): continue
        if start is None: start = rec["t"]
        n = sum(1 for p in rec["procs"] if p["comm"].startswith(("chrom","chrome")))
        counts.append(((rec["t"]-start)/1e6, n))
    peak = max(c for _,c in counts)
    first_peak = next(s for s,c in counts if c==peak)
    last_peak = max(s for s,c in counts if c==peak)
    samples_at_peak = sum(1 for _,c in counts if c==peak)
    med = sorted(c for _,c in counts)[len(counts)//2]
    by10 = [max(c for s,c in counts if lo<=s<lo+10) if any(lo<=s<lo+10 for s,_ in counts) else None for lo in range(0,310,10)]
    print(rd.name, "peak", peak, "first/last at s", round(first_peak,1), round(last_peak,1), "samples at peak", samples_at_peak, "of", len(counts), "median count", med)
    print("   max per 10s bucket:", by10)
