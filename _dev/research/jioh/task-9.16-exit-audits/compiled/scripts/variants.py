import json, pathlib, sys
sys.path.insert(0, '.')
from facts import file_facts, B
def chain(F):
    ch=[t for t in F['tasks'] if 'loop_cpu' in t]
    return sum(t['loop_cpu'] for t in ch), {t['id']:t['loop_cpu'] for t in ch}
for base in ['c2-p2a','c2-p2b','c7-gaming']:
    fb=file_facts(base); sb,mb=chain(fb)
    for v in ['chain-x1.2','chain-x1.4','venue-x0.8','venue-x1.25']:
        fv=file_facts(f'{base}@{v}'); sv,mv=chain(fv)
        other={t['id']:(t.get('cpu'),) for t in fv['tasks'] if 'cpu' in t}
        otherb={t['id']:(t.get('cpu'),) for t in fb['tasks'] if 'cpu' in t}
        print(base, v, 'chain', sb, '->', sv, f'{sv/16667:.4f} lanes', 'ratio', round(sv/sb,4), '| other cpu ratios', {k: round(other[k][0]/otherb[k][0],4) for k in other if otherb.get(k) and otherb[k][0]})
# venue on a non-gaming file: RUN scaling
for base in ['c1-render','c7-dev']:
    fb=file_facts(base)
    for v in ['venue-x0.8','venue-x1.25']:
        fv=file_facts(f'{base}@{v}')
        print(base, v, {t['id']: round(t['cpu']/[x for x in fb['tasks'] if x['id']==t['id']][0]['cpu'],4) for t in fv['tasks'] if 'cpu' in t and t['cpu']}, 'T_end', fb['t_end'], fv['t_end'])
for base in ['c2-p1a','c2-p2a']:
    for v in ['seg1-30s','seg1-120s']:
        fv=file_facts(f'{base}@{v}')
        print(base, v, [(s['t_start']/1e6, s['t_end']/1e6, s['mode']) for s in fv['ground_truth']])
