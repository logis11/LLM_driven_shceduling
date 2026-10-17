import json, pathlib, sys
sys.path.insert(0,'.')
from facts import file_facts, B
ids=[p.name[:-14] for p in sorted(B.glob('*.workload.json'))]
for fid in ids:
    with open(B/f'{fid}.workload.json','rb') as fh:
        if b'.chain.' not in fh.read(): continue
    F=file_facts(fid)
    ch=[t for t in F['tasks'] if 'loop_cpu' in t]
    head=[t for t in ch if t.get('loop_period')][0]
    P=head['loop_period']; a=head['arrive']; T=min(F['t_end'], head['depart'] or F['t_end'])
    k=(T-a)//P; last=a+k*P; s=sum(t['loop_cpu'] for t in ch)
    print(f"{fid:<28} T_end={F['t_end']} last_tick={last} T_end-last={T-last:>6} chain={s:>6} feasible_if_uninterrupted={T-last>=s} margin={T-last-s}")
