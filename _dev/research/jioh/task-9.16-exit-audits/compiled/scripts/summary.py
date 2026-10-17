import json,glob,os,collections
for p in sorted(glob.glob('facts/*.json')):
    F=json.load(open(p))
    segs=' | '.join(f"{s['t_start']/1e6:g}-{s['t_end']/1e6:g}s {s['mode']} {s.get('attributes')}" for s in F['ground_truth'])
    print(f"== {F['id']} T_end={F['t_end']/1e6:g}s :: {segs}")
    chain=[t for t in F['tasks'] if 'loop_cpu' in t]
    if chain:
        heads=[t for t in chain if t.get('loop_period')]
        for h in heads:
            pre=h['id'].split('.chain.')[0]
            mem=[t for t in chain if t['id'].startswith(pre+'.')]
            s=sum(t['loop_cpu'] for t in mem)
            stages=sorted((t['loop_cpu'] for t in mem),reverse=True)
            print(f"   CHAIN {pre}: members={len(mem)} sum={s} period={h['loop_period']} slack={h['loop_period']-s} lanes={s/h['loop_period']:.4f} head={h['loop_cpu']} top={stages[:6]} classes={set(t['class'] for t in mem)}")
    for t in F['tasks']:
        if 'loop_cpu' in t: continue
        x=f"   {t['id']:<14} {t['name']:<16} {t['class']:<6} arr={t['arrive']/1e6:g} dep={(t['depart'] or 0)/1e6:g} cpu={t['cpu']/1e6:.3f}s"
        if t.get('timer_period'): x+=f" TIMER{t['timer_period']} cyc_med={t.get('cycle_med')} max={t.get('cycle_max')} >10ms={t.get('cycle_ge_slice')}/{t.get('cycles_n')}"
        else: x+=f" b1batch={t['b1_batch_cpu_frac']:.3f} burst_med={t.get('burst_med')} max={t.get('burst_max')} sleep_med={t.get('sleep_med')} sleep_tot={t['sleep_total']/1e6:.3f}s"
        if 'keystroke_n' in t: x+=f" KEYS n={t['keystroke_n']} med={t['keystroke_med']} mean={t['keystroke_mean']:.0f} >=10ms={t['keystroke_ge_slice']}"
        if 'spawn_n' in t: x+=f" SPAWN n={t['spawn_n']} cap={t['fork_cap']} cpu={t['spawn_cpu']/1e6:.3f}s b1batch={t['spawn_b1_batch_cpu']/max(1,t['spawn_cpu']):.3f} never_batch={t['spawn_children_never_batch']} classes={t['spawn_classes']}"
        print(x)
    w=collections.Counter()
    for k,v in F['wakes'].items():
        tg,ch=k.split('|')
        if ch=='input': print(f"   INPUT {tg}: n={v['n']} first={v['first']/1e6:.3f}s last={v['last']/1e6:.3f}s")
