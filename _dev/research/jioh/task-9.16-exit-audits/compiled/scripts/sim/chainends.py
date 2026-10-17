import json, subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
B = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single')
fid, name, T = sys.argv[1], sys.argv[2], int(sys.argv[3])
tr = subprocess.run([str(here/'simbin'), str(B/f'{fid}.workload.json'), str(here/f'{fid}.{name}.schedule.json')], capture_output=True, text=True)
ticks=[]; ends=[]; last=None
for line in tr.stdout.splitlines():
    ev = json.loads(line)
    if ev.get('task') == 'game.chain.1' and ev.get('event') == 'ready' and ev.get('cause') == 'timer_tick' and ev['t'] <= T: ticks.append(ev['t'])
    if ev.get('task') == 'game.chain.16' and ev.get('event') == 'run_end' and ev['t'] <= T: ends.append((ev['t'], ev.get('reason')))
print(fid, name, 'head timer_tick ready lines <= T_end', len(ticks), 'last', ticks[-1] if ticks else None, '| tail run_end <= T_end', len(ends), 'last', ends[-1] if ends else None)
