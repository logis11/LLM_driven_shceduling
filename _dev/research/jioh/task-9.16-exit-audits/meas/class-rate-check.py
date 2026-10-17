import yaml,sys
W=[.01,.04,.05,.15,.25,.25,.15,.05,.04,.009,.001]
d=yaml.safe_load(open(sys.argv[1]))['archetypes']
def tmean(t): return sum(w*m for w,m in zip(W,t['means']))
worst=[]
for a,e in d.items():
    p=e.get('params') or {}
    groups=[('components',p.get('components') or [])]+[('focus',p.get('focus_components') or [])]
    for name,op in (p.get("operations") or {}).items():
        groups.append(('op:'+name,op.get('components') or []))
    for g,comps in groups:
        for c in comps:
            if 'gap' not in c or 'wakes_per_s' not in c: continue
            m=tmean(c['gap']); r=1e6/m
            rel=r/c['wakes_per_s']-1
            worst.append((abs(rel),a,g,c['comm'],round(c['wakes_per_s'],5),round(r,5)))
worst.sort(reverse=True)
print(len(worst),"components"); 
for w in worst[:8]: print(w)
