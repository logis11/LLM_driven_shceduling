import json, subprocess, sys, collections, pathlib
here = pathlib.Path(__file__).parent
B = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single')
fid, name = sys.argv[1], sys.argv[2]
tr = subprocess.run([str(here/'simbin'), str(B/f'{fid}.workload.json'), str(here/f'{fid}.{name}.schedule.json')], capture_output=True, text=True)
T_end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**15
cpu = collections.Counter(); start = {}; tail_done = []; ticks = []; lines = 0
for line in tr.stdout.splitlines():
    ev = json.loads(line); lines += 1
    e = ev.get('event')
    if e == 'run_start': start[ev['task']] = ev['t']
    elif e == 'run_end' and ev['task'] in start:
        a = start.pop(ev['task']); b = min(ev['t'], T_end)
        if b > a: cpu[ev['task']] += b - a
    elif e == 'deadline' and ev['task'].endswith('chain.1') and ev['t'] <= T_end: ticks.append(ev)
print(fid, name, 'lines', lines, {k: round(v/1e6, 3) for k, v in cpu.items() if 'chain' not in k}, 'chain', round(sum(v for k,v in cpu.items() if 'chain' in k)/1e6,3))
if ticks: print(' head deadline lines', len(ticks), 'missed', sum(not t['met'] for t in ticks))
