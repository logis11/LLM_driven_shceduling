"""9.16 compiled-number audit: per-file, per-task facts from the final build.
Usage: facts.py [file-id ...]  -> writes facts/<id>.json (default: all 51 core files + needed variants)."""
import json, sys, os, collections, statistics as st, pathlib
R = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling')
B = R/'dataset/build/coreset-single'
OUT = pathlib.Path(__file__).parent/'facts'; OUT.mkdir(exist_ok=True)
SLICE = 10000
BLOCK = {'SLEEP', 'WAIT', 'TIMER'}

def flat(prog):
    for s in prog:
        if s['op'] == 'LOOP':
            if s['count'] == 'unbounded':
                yield {'op': 'LOOP*', 'body': list(flat(s['body']))}
            else:
                for _ in range(int(s['count'])):
                    yield from flat(s['body'])
        else:
            yield s

def q(xs, p):
    xs = sorted(xs)
    if not xs: return None
    k = (len(xs)-1)*p; f = int(k); c = min(f+1, len(xs)-1)
    return xs[f] + (xs[c]-xs[f])*(k-f)

def task_facts(e, t0, tend):
    prog = list(flat(e['program']))
    f = {'id': e['id'], 'name': e['name'], 'class': e.get('declared_class'), 'arrive': t0,
         'depart': e.get('depart'), 'ops': dict(collections.Counter(s['op'] for s in prog))}
    loop = [s for s in prog if s['op'] == 'LOOP*']
    if loop:
        body = loop[0]['body']
        f['loop_body'] = body
        f['loop_cpu'] = sum(s['us'] for s in body if s['op'] == 'RUN')
        per = [s['period_us'] for s in body if s['op'] == 'TIMER']
        f['loop_period'] = per[0] if per else None
        f['wake_targets'] = [s['target'] for s in body if s['op'] == 'WAKE']
        return f
    runs = [s['us'] for s in prog if s['op'] == 'RUN']
    f['cpu'] = sum(runs)
    f['n_run'] = len(runs)
    sl = [s['us'] for s in prog if s['op'] == 'SLEEP']
    f['sleep_total'] = sum(sl)
    if sl: f['sleep_med'] = st.median(sl); f['sleep_max'] = max(sl)
    per = [s['period_us'] for s in prog if s['op'] == 'TIMER']
    f['timer_period'] = sorted(set(per))
    f['wake_targets'] = sorted(set(s['target'] for s in prog if s['op'] == 'WAKE'))
    # bursts: CPU between blocking ops (alone approximation: every WAIT/SLEEP/TIMER blocks)
    bursts, cur, batch = [], 0, 0
    after_input, kc = False, []
    cyc, cycles = None, []
    for s in prog:
        if s['op'] == 'RUN':
            b0 = cur; cur += s['us']
            batch += max(0, cur - SLICE) - max(0, b0 - SLICE)
            if after_input: kc[-1] += s['us']
            if cyc is not None: cyc += s['us']
        elif s['op'] in BLOCK:
            if cur: bursts.append(cur)
            cur = 0
            after_input = s['op'] == 'WAIT' and s.get('channel', '').startswith('input')
            if after_input: kc.append(0)
            if s['op'] == 'TIMER':
                if cyc is not None: cycles.append(cyc)
                cyc = 0
    if cur: bursts.append(cur)
    if cyc is not None: cycles.append(cyc)
    f['bursts_n'] = len(bursts)
    if bursts:
        f['burst_med'] = st.median(bursts); f['burst_max'] = max(bursts)
        f['burst_ge_slice'] = sum(b >= SLICE for b in bursts)
    f['b1_batch_cpu_frac'] = batch / f['cpu'] if f['cpu'] else 0.0
    f['b1_batch_cpu'] = batch
    if kc:
        f['keystroke_n'] = len(kc); f['keystroke_med'] = st.median(kc); f['keystroke_mean'] = st.mean(kc)
        f['keystroke_ge_slice'] = sum(k >= SLICE for k in kc)
    if cycles:
        f['cycles_n'] = len(cycles)
        f['cycle_deciles'] = [q(cycles, p/10) for p in range(1, 10)]
        f['cycle_max'] = max(cycles); f['cycle_med'] = st.median(cycles)
        f['cycle_gt_slice'] = sum(c > SLICE for c in cycles); f['cycle_ge_slice'] = sum(c >= SLICE for c in cycles)
        if per: f['cycle_gt_period'] = sum(c > per[0] for c in cycles)
        f['cycle_list_head'] = cycles[:5]
    if 'spawn_table' in e:
        f['fork_cap'] = e.get('fork_cap')
        f['spawn_n'] = len(e['spawn_table'])
        ch = [task_facts(c, None, tend) for c in e['spawn_table']]
        f['spawn_cpu'] = sum(c.get('cpu', 0) for c in ch)
        f['spawn_b1_batch_cpu'] = sum(c.get('b1_batch_cpu', 0) for c in ch)
        f['spawn_names'] = dict(collections.Counter(c['name'] for c in ch))
        f['spawn_classes'] = dict(collections.Counter(c['class'] for c in ch))
        f['spawn_child_cpu_med'] = st.median([c.get('cpu', 0) for c in ch])
        f['spawn_child_cpu_max'] = max(c.get('cpu', 0) for c in ch)
        f['spawn_children_never_batch'] = sum(1 for c in ch if c.get('b1_batch_cpu', 0) == 0)
    return f

def file_facts(fid):
    d = json.load(open(B/f'{fid}.workload.json'))
    gt = d['ground_truth']
    tend = max(s['t_end'] for s in gt)
    F = {'id': fid, 'meta': d['meta'], 'ground_truth': gt, 'focus': d['focus'], 't_end': tend, 'tasks': [], 'wakes': {}}
    wk = collections.defaultdict(list)
    for e in d['events']:
        if e['op'] == 'arrive':
            F['tasks'].append(task_facts(e, e['t'], tend))
        elif e['op'] == 'wake':
            wk[(e['target'], e['channel'].split(':')[0])].append(e['t'])
        else:
            F.setdefault('other_ops', collections.Counter())[e['op']] += 1
    for (tg, ch), ts in wk.items():
        F['wakes'][f'{tg}|{ch}'] = {'n': len(ts), 'first': min(ts), 'last': max(ts), 'times': ts if ch == 'input' else None}
    return F

if __name__ == '__main__':
    ids = sys.argv[1:] or sorted(p.name[:-len('.workload.json')] for p in B.glob('*.workload.json') if '@' not in p.name)
    for fid in ids:
        F = file_facts(fid)
        json.dump(F, open(OUT/f'{fid}.json', 'w'), default=dict)
        print('done', fid, flush=True)
