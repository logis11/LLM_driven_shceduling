import re, pathlib, sys, collections, json
sys.path.insert(0,'.'); import analyze_head as A
is_chrome = lambda c: c.startswith(("chrom","chrome"))
is_el = lambda c: c.lower().startswith("element")
for rd in sorted(pathlib.Path('gui').iterdir()):
    tid_type = {}
    for line in (rd/'lifecycle.log').open(errors='replace'):
        parts = line.split()
        if len(parts) < 4 or parts[1] not in ('exit',): continue
        m = re.search(r'--type=([a-z-]+)', line)
        sub = re.search(r'--utility-sub-type=([A-Za-z._]+)', line)
        rid = re.search(r'--renderer-client-id=(\d+)', line)
        webui = '--top-chrome-webui' in line
        if m:
            tid_type.setdefault(int(parts[2]), m.group(1) + ('/'+sub.group(1).split('.')[0] if sub else '') + ('/rid'+rid.group(1) if rid else '') + ('/webui' if webui else ''))
        elif re.search(r'(chrome|element-desktop) --(?!type)', line) and '--type' not in line:
            tid_type.setdefault(int(parts[2]), 'browser')
    ph = A.load_phases(rd)
    for phase, match, key in (("chromium-10-tabs", is_chrome, "chromium_wakes"), ("element-idle", is_el, "element_wakes")):
        ws = []
        series = {}
        for rec in A.iter_samples(rd):
            t = A.hms_us(rec["t"])
            if not A.in_phase(t, ph[phase]): continue
            for p in rec["procs"]:
                if match(p["comm"]) and p.get("vctxt") is not None:
                    k=(p["pid"],p["starttime"]); e=series.setdefault(k,{"t0":t,"v0":p["vctxt"],"c0":p["utime"]+p["stime"],"thr":p["threads"]})
                    e.update(t1=t,v1=p["vctxt"],c1=p["utime"]+p["stime"])
        out=[]
        for (pid,_),e in series.items():
            span=e["t1"]-e["t0"]; wk=e["v1"]-e["v0"]
            if span<5 or wk<5: continue
            typ = tid_type.get(pid)
            if typ is None:
                cands=[tid_type[x] for x in range(pid+1,pid+20) if x in tid_type]
                typ = (collections.Counter(cands).most_common(1)[0][0]+"?") if cands else "?"
            out.append(f"{typ}:{span*1e3/wk:.0f}ms")
        print(rd.name, phase, out)
