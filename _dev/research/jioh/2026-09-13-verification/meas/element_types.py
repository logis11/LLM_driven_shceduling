import re, pathlib, sys, collections
sys.path.insert(0,'.'); import analyze_head as A
for rd in sorted(pathlib.Path('gui').iterdir()):
    ph = A.load_phases(rd); w = ph["element-idle"]
    groups = collections.defaultdict(lambda: [0, None])
    other = collections.Counter()
    for line in (rd/'lifecycle.log').open(errors='replace'):
        m = A._EXIT.match(line)
        if not m: continue
        t, pid, dur, cmd = m.groups()
        if not (w[0] <= A.hms_str(t) <= w[1]+3): continue
        if 'element' not in cmd.lower() and 'electron' not in cmd.lower(): continue
        typ = re.search(r'--type=([a-z-]+)', cmd); sub = re.search(r'--utility-sub-type=([A-Za-z._]+)', cmd)
        key = (typ.group(1) if typ else 'main/none') + ('/' + sub.group(1) if sub else '')
        g = groups[key]; g[0] += 1; g[1] = dur
    print(rd.name, dict((k, (v[0], v[1])) for k, v in groups.items()))
