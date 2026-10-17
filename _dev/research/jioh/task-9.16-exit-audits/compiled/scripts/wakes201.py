import json, pathlib, subprocess, collections
B = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build')
files = sorted(B.glob('*/*.workload.json'))
print('total files', len(files), collections.Counter(p.parent.name for p in files))
hit = collections.Counter(); total = 0; nfiles = 0; per = {}
for p in files:
    with open(p, 'rb') as fh:
        data = fh.read()
    if b'spawn_table' not in data: continue
    d = json.loads(data)
    n = 0
    for e in d['events']:
        if e['op'] != 'arrive' or 'spawn_table' not in e: continue
        ids = {c['id'] for c in e['spawn_table']}
        for c in e['spawn_table']:
            for s in c['program']:
                if s['op'] == 'WAKE' and s['target'] in ids: n += 1
    if n:
        nfiles += 1; total += n
        hit[p.parent.name + ('@' if '@' in p.name else '')] += 1
        per[p.name] = n
print('files with child->child WAKE', nfiles, dict(hit), 'total', total)
print({k: v for k, v in per.items() if 'coreset' in k or '@' in k or k.startswith('c')})
pre = collections.Counter(k.split('-')[0] for k in per)
print(pre)
