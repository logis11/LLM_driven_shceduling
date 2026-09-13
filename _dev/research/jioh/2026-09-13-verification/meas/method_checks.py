import re, json, pathlib, collections, sys, datetime, math, statistics
sys.path.insert(0, '.')
import analyze_head as A
base = pathlib.Path(sys.argv[1])
for rd in sorted(base.iterdir()):
    ph = A.load_phases(rd)
    for bp in ("kernel-build-j8", "kernel-build-cold"):
        w = A.good(ph, bp)
        if not w: continue
        durfmt = collections.Counter(); byname = collections.defaultdict(list); unparsed = collections.Counter()
        for line in (rd/"lifecycle.log").open(errors="replace"):
            m = A._EXIT.match(line)
            if not m: continue
            t, pid, dur_text, cmd = m.groups()
            b = pathlib.PurePath(cmd.split()[0]).name if cmd else ""
            if b not in A.COMPILER_NAMES: continue
            d = A.parse_duration_us(dur_text)
            if d is None:
                # compute approx birth anyway for m/h
                unparsed[(b, dur_text[-1])] += 1
                continue
            birth = A.hms_str(t) - d/1e6
            if w[0] <= birth <= w[1]:
                byname[b].append(max(d,1000))
        tot = sum(len(v) for v in byname.values())
        print(rd.name, bp, "total", tot, "unparsed(non-s) compiler exits anywhere:", dict(unparsed))
        for b, v in sorted(byname.items(), key=lambda x: -len(x[1])):
            logs = [math.log(x) for x in v]
            print(f"   {b:10s} n={len(v):6d} median_us={round(math.exp(statistics.mean(logs))):8d} sl={statistics.stdev(logs) if len(v)>1 else 0:.3f} floored1ms={sum(1 for x in v if x==1000)}")
