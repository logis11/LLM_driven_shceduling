import json, collections, sys
d=json.load(open(sys.argv[1]))
types=d['types']; E=d['entries']
tc=collections.Counter(r.get('type','<no type>') for f,i,r in E)
print('entries per type (all files):')
for t,c in tc.most_common(): print(f'  {t!r}: {c}', '' if t in types or t=='<no type>' else '  <-- UNDEFINED')
print('defined but unused:', [t for t in types if tc[t]==0])
undefined=[(f,i,r) for f,i,r in E if 'type' in r and r['type'] not in types]
print('undefined type entries:', len(undefined))
for u in undefined: print('  ',u)
names=[r['name'] for f,i,r in E if 'name' in r]
print('names total', len(names), 'distinct', len(set(names)))
c=collections.Counter(names); dup={n:k for n,k in c.items() if k>1}
print('duplicated names', len(dup), 'extra occurrences', sum(k-1 for k in dup.values()))
keys=collections.Counter(k for f,i,r in E for k in r)
print('keys used', dict(keys))
notype=[(f,i,r) for f,i,r in E if 'type' not in r]
print('entries w/o type', len(notype))
# schema checks
enum_sched={"fifo","rr","normal","batch","idle"}; enum_io={"best-effort","realtime","idle","none"}
bad=[]
for f,i,r in E:
    for k,v in r.items():
        if k in('nice','latency_nice') and not(isinstance(v,int) and -20<=v<=19): bad.append((f,i,k,v))
        if k=='ionice' and not(isinstance(v,int) and 0<=v<=7): bad.append((f,i,k,v))
        if k=='sched' and v not in enum_sched: bad.append((f,i,k,v))
        if k=='ioclass' and v not in enum_io: bad.append((f,i,k,v))
        if k=='oom_score_adj' and not(isinstance(v,int) and -1000<=v<=1000): bad.append((f,i,k,v))
        if k in ('name','type','cgroup','cpuset') and not isinstance(v,str): bad.append((f,i,k,v))
print('schema value violations', len(bad)); [print('  ',b) for b in bad]
# per top-level dir
dc=collections.defaultdict(collections.Counter)
fc=collections.Counter()
for f,i,r in E:
    p=f.split('/'); key='/'.join(p[1:3]) if p[1]=='Games' and len(p)>3 and p[2] in('linux-native','wine_proton') else p[1]
    dc[key][r.get('type','<none>')]+=1
for k in sorted(dc): print(k, sum(dc[k].values()), dict(dc[k].most_common()))
