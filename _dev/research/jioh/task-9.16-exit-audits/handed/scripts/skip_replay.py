"""Independent replay of mock-media's run file: one lane, FIFO, run to block,
TIMER under the skip rule (memo 2026-10-07 §1, t0 = the first TIMER execution
= arrival). Emits deadline lines (t, task, due, met, slack) and timer_tick
ready times, to compare with the fixture's trace.jsonl."""
import json, sys
run = json.load(open(sys.argv[1])); T_END = 95000
tasks = {}
for e in run['events']:
    body = e['program'][0]['body'] if e['program'][0]['op'] == 'LOOP' else None
    tasks[e['id']] = dict(arrive=e['t'], depart=e.get('depart'), body=body,
                          prog=e['program'], P=body[0]['period_us'] if body else None)
out, ready_q, t = [], [], 0
state = {}
def reach_timer(tid, now, first=False):
    s = state[tid]; P = s['P']
    nxt = s['next']  # next unconsumed tick index
    if s['t0'] + nxt * P > now:
        s['block_until'] = s['t0'] + nxt * P; return False
    m = (now - s['t0']) // P
    for k in range(nxt, m):  # skipped
        out.append(('deadline', now, tid, s['t0'] + (k + 1) * P, False, s['t0'] + (k + 1) * P - now, 'skipped'))
    out.append(('ready_timer_tick', now, tid)); s['cur'] = m; s['next'] = m + 1
    return True
events = sorted([(v['arrive'], i, k) for i, (k, v) in enumerate(tasks.items())])
pending = list(events)
lane_free_at = 0
while True:
    # admit arrivals and timer wakes up to t
    for a in [p for p in pending if p[0] <= t]:
        pending.remove(a); tid = a[2]; v = tasks[tid]
        if v['P']:
            state[tid] = dict(P=v['P'], t0=a[0], next=0, block_until=None)
            reach_timer(tid, a[0]); ready_q.append((a[0], a[1], tid))
        else:
            state[tid] = dict(P=None, left=v['prog'][0]['us']); ready_q.append((a[0], a[1], tid))
    for tid, s in state.items():
        if s.get('block_until') is not None and s['block_until'] <= t:
            bu = s['block_until']; s['block_until'] = None
            out.append(('ready_timer_tick', bu, tid)); s['cur'] = s['next']; s['next'] += 1
            ready_q.append((bu, list(tasks).index(tid), tid))
    if t >= T_END: break
    if not ready_q:
        cands = [p[0] for p in pending] + [s['block_until'] for s in state.values() if s.get('block_until')]
        if not cands: break
        t = min(cands); continue
    ready_q.sort(); _, _, tid = ready_q.pop(0); s = state[tid]
    if s['P'] is None:
        t += s['left']; s['left'] = 0; continue
    while True:  # run one job, then reach TIMER
        t += tasks[tid]['body'][1]['us']
        due = s['t0'] + (s['cur'] + 1) * s['P']
        out.append(('deadline', t, tid, due, t <= due, due - t, 'job %d' % s['cur']))
        if not reach_timer(tid, t): break
        # consumed at once: keeps the lane (FIFO, run to block)
for o in out: print(o)
