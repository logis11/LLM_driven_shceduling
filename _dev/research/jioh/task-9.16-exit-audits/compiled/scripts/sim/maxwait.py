import json, subprocess, sys, pathlib, collections
here = pathlib.Path(__file__).parent
B = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single')
fid, name, T = sys.argv[1], sys.argv[2], int(sys.argv[3])
tr = subprocess.Popen([str(here/'simbin'), str(B/f'{fid}.workload.json'), str(here/f'{fid}.{name}.schedule.json')], stdout=subprocess.PIPE, text=True)
ready = {}; mx = collections.Counter()
for line in tr.stdout:
    ev = json.loads(line); e = ev.get('event'); tk = ev.get('task')
    if e == 'ready' and tk not in ready: ready[tk] = ev['t']
    elif e == 'run_start' and tk in ready:
        w = min(ev['t'], T) - ready.pop(tk); mx[tk] = max(mx[tk], w)
for tk, t0 in ready.items():
    if t0 < T: mx[tk] = max(mx[tk], T - t0)
print(fid, name, 'longest ready wait (s):', {k: round(v/1e6, 3) for k, v in mx.most_common(5)})
