import re, pathlib, collections, sys
sys.path.insert(0,'.'); import analyze_head as A
for rd in sorted(pathlib.Path('gui').iterdir()):
    ph = A.load_phases(rd); w = ph["chromium-10-tabs"]
    rids = collections.defaultdict(list)
    for line in (rd/'lifecycle.log').open(errors='replace'):
        if '--type=renderer' not in line: continue
        m = A._EXIT.match(line)
        if not m: continue
        t, pid, dur, cmd = m.groups()
        if not A.in_phase(A.hms_str(t), (w[0], w[1]+2)): continue
        mm = re.search(r"--renderer-client-id=(\d+)", cmd)
        if not mm: continue
        rid = mm.group(1)
        d = A.parse_duration_us(dur)
        rids[int(rid)].append(d if d is not None else dur)
    short = {r: max(v, key=lambda x: x if isinstance(x,int) else 10**12) for r, v in rids.items()}
    s = sorted(r for r,v in short.items() if isinstance(v,int) and v < 2_000_000)
    l = sorted(r for r,v in short.items() if not (isinstance(v,int) and v < 2_000_000))
    print(rd.name, "renderer client ids exiting <2s:", s, " long-lived:", {r: short[r] for r in l})
