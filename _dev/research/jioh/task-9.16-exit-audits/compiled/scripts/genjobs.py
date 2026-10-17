import json, pathlib, collections
B = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build')
bad = []; n = 0; files = 0; minmargin = None
for d in sorted(B.glob('*-single')):
    if d.name == 'coreset-single': continue
    for p in sorted(d.glob('*.workload.json')):
        w = json.load(open(p)); files += 1
        T = max(s['t_end'] for s in w['ground_truth'])
        for e in w['events']:
            if e['op'] != 'arrive' or e.get('depart') is not None: continue
            ops = e['program']
            if any(s['op'] == 'LOOP' for s in ops): continue
            cpu = sum(s['us'] for s in ops if s['op'] == 'RUN'); sl = sum(s['us'] for s in ops if s['op'] == 'SLEEP')
            sp = sum(sum(s['us'] for s in c['program'] if s['op']=='RUN') for c in e.get('spawn_table', []))
            n += 1
            m = T - (e['t'] + cpu + sl)
            if minmargin is None or m < minmargin[0]: minmargin = (m, p.name, e['id'])
            if m < 0: bad.append((p.name, e['id'], e['t'], cpu, sl, T))
print('generated files', files, 'batch tasks', n, 'own CPU+sleep past T_end', len(bad), 'min margin', minmargin)
print(bad[:10])
