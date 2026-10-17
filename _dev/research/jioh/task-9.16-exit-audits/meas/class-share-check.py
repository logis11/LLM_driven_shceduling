import yaml,sys,re
W=[.01,.04,.05,.15,.25,.25,.15,.05,.04,.009,.001]
d=yaml.safe_load(open(sys.argv[1]))['archetypes']
def tmean(t): return sum(w*m for w,m in zip(W,t['means']))
for a,e in d.items():
    p=e.get('params') or {}
    comps=p.get('components')
    if not comps: continue
    share=sum(c['wakes_per_s']*tmean(c['run']) for c in comps if 'run' in c)/1e6
    rate=sum(c['wakes_per_s'] for c in comps)
    stats=(e.get('validation_stats') or {}).get('stats') or []
    st=[s for s in stats if re.search(r'(idle|steady|shown|play)\b.*(cpu-share|wakes/s)',s) and not s.startswith('driven')]
    print(f"{a:20s} share {share:.6f} rate {rate:.4f} | {st}")
