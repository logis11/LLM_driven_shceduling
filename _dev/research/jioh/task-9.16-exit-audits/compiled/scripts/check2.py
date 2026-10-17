import json, pathlib, collections
R = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling'); B = R/'dataset/build/coreset-single'
def F(f): return json.load(open(f'facts/{f}.json'))
def rep(f): return json.load(open(B/f'{f}.report.json'))
print('## operations per report')
for f in ['c1-browsing','c7-browsing','c1-office','c7-office','c1-dev','c7-dev','c1-indexing','c7-indexing','c1-mail','c7-mail']:
    print(f, rep(f).get('operations'))
print('## input wakes in base first 26.385 s / counterpart')
for b, c, cut in [('c1-browsing','c7-browsing',26385000),('c1-office','c7-office',26385000),('c1-dev','c7-dev',26385000),('c1-mail','c7-mail',26385000),('c1-indexing','c7-indexing',39435000)]:
    bt=[v for k,v in F(b)['wakes'].items() if k.endswith('|input')][0]['times']
    ci=[v for k,v in F(c)['wakes'].items() if k.endswith('|input')]
    ct=ci[0]['times'] if ci else []
    inb=[t for t in bt if t < cut]
    print(b, len(bt), 'in cut', len(inb), '|', c, len(ct), 'same times' , sorted(ct)==sorted(inb), 'base-not-in-cp', len(set(inb)-set(ct)))
print('## manifest demand')
m = json.load(open(R/'dataset/build.manifest.json'))['demand']
def u(f): return m[f'coreset-single/{f}.workload.json']
for f in ['c2-p1a','c2-p1b','c2-p2a','c2-p2b','c2-p3a','c2-p3b','c2-p2a-idle']:
    print(f, u(f)['utilization'], u(f)['demand_class'], [round(s['utilization'],4) for s in u(f)['segments']])
for mode in ['browsing','office','mail','dev','photo','meeting','gaming','media','video-edit','compile','ml-train','render','transcode','indexing','backup','idle']:
    print(f'c7-{mode} {u("c7-"+mode)["utilization"]:.4f} / c1-{mode} {u("c1-"+mode)["utilization"]:.4f}', u('c7-'+mode)['demand_class'])
print('## all demand classes', collections.Counter(v['demand_class'] for v in m.values()))
print('## segments grid')
segs=[]; pcm=[]
for p in sorted(B.glob('*.workload.json')):
    if '@' in p.name: continue
    fid=p.name[:-14]; fa=F(fid)
    for s in fa['ground_truth']:
        bw=s.get('attributes',{}).get('background_wanted')
        segs.append((fid,s['mode'],bw,s['t_start'],s['t_end']))
        if s.get('attributes',{}).get('pre_committed_miss'): pcm.append((fid,s['mode'],bw,s['t_start']/1e6))
print('segments', len(segs), 'ambiguous', sum(1 for s in segs if s[1]=='ambiguous'), 'false', sum(1 for s in segs if s[2] is False), 'true', sum(1 for s in segs if s[2] is True))
print('pcm', len(pcm), pcm)
cells=collections.Counter((s[1],s[2]) for s in segs if s[1]!='ambiguous'); print('cells', len(cells))
print('## c6-dual gt', F('c6-dual')['ground_truth'])
