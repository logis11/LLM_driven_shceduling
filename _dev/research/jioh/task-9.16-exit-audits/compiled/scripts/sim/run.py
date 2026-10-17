import json, subprocess, sys, collections, pathlib
R = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling')
SIM = pathlib.Path(__file__).parent/'simbin'; B = R/'dataset/build/coreset-single'; OUT = pathlib.Path(__file__).parent
CFG = {'fixed': {'algorithm':'MLFQ','params':{'num_queues':3,'timeslice_us':10000,'timeslice_growth':2,'boost_interval_us':100000}},
       'edf':   {'algorithm':'EDF','params':{'residual_timeslice_us':10000}}}
for fid in sys.argv[1:]:
    for name, cfg in CFG.items():
        sch = {'workload_id': fid, 'condition': name, 'schedule': [{'t_us': 0, 'provenance': 'fallback', 'config': dict(cfg, batch_bandwidth_cap=None)}]}
        sp = OUT/f'{fid}.{name}.schedule.json'; json.dump(sch, open(sp,'w'))
        tr = subprocess.run([str(SIM), str(B/f'{fid}.workload.json'), str(sp)], capture_output=True, text=True)
        if tr.returncode: print(fid, name, 'FAIL', tr.stderr[:300]); continue
        dl = collections.defaultdict(lambda: [0,0]); maxwait = collections.Counter()
        for line in tr.stdout.splitlines():
            ev = json.loads(line)
            if ev.get('event') == 'deadline':
                dl[ev['task']][0] += 1; dl[ev['task']][1] += (not ev['met'])
        print(fid, name, {k: f'{v[1]}/{v[0]} missed ({v[1]/v[0]:.3%})' for k, v in dl.items()})
