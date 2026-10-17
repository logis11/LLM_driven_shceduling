"""Replay one task alone (it runs whenever it is runnable): CPU intervals on the wall clock."""
import json, pathlib, collections, bisect, sys
B = pathlib.Path('/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single')
def load(fid): return json.load(open(B/f'{fid}.workload.json'))
def alone(d, tid):
    e = [x for x in d['events'] if x['op']=='arrive' and x['id']==tid][0]
    wk = collections.defaultdict(list)
    for x in d['events']:
        if x['op']=='wake' and x['target']==tid: wk[x['channel']].append(x['t'])
    for v in wk.values(): v.sort()
    ptr = collections.Counter(); t = e['t']; iv = []; dep = e.get('depart')
    for s in e['program']:
        if s['op']=='RUN':
            iv.append((t, t+s['us'])); t += s['us']
        elif s['op']=='SLEEP': t += s['us']
        elif s['op']=='WAIT':
            c = s['channel']; L = wk.get(c, [])
            i = ptr[c]
            # mailbox: wakes are remembered; consume the next wake in order
            if i >= len(L): break
            t = max(t, L[i]); ptr[c] += 1
        elif s['op']=='TIMER':
            pass
    return iv, t
def cpu_in(iv, a, b): return sum(max(0, min(y,b)-max(x,a)) for x,y in iv)
if __name__=='__main__':
    # c2-p3b editor CPU in 60-326 s, backup idle lane
    d=load('c2-p3b'); iv,_=alone(d,'editor')
    ed=cpu_in(iv,60e6,326e6); print('c2-p3b editor cpu 60-326 s', ed/1e6, 'idle lane', (266e6-ed)/1e6)
    d=load('c1-backup'); iv,_=alone(d,'editor'); ed=cpu_in(iv,2e6,277e6); print('c1-backup editor cpu 2-277', ed/1e6, 'idle lane', (275e6-ed)/1e6, 'backup needs cpu+sleep', 165.668+0.315)
    d=load('c7-backup'); iv,_=alone(d,'editor'); ed=cpu_in(iv,0,165.668e6); print('c7-backup editor cpu', ed/1e6, 'idle lane', (165.668e6-ed)/1e6)
    for f,tid,job,start,T in [('c1-compile','editor',1315.907,2e6,1594e6),('c1-ml-train','editor',1389.885+0.012,2e6,1612e6),('c1-transcode','video-editor',2970.871+0.522,2e6,4762e6),('c1-render','editor',16.545+0.008,2e6,60e6),('c2-p3a','editor',16.545+0.048,60e6,326e6),('c1-indexing','editor',39.435+6.065,2e6,60e6)]:
        d=load(f); iv,_=alone(d,tid); ed=cpu_in(iv,start,T)
        print(f, 'editor cpu in job span', round(ed/1e6,3), 'job cpu(+sleep)', job, 'lane', (T-start)/1e6, 'margin s', round((T-start)/1e6-ed/1e6-job,3))
    d=load('c3-creation'); iv,_=alone(d,'video-editor'); print('c3-creation kdenlive cpu 240-3212 s', cpu_in(iv,240e6,3212e6)/1e6, 'share', cpu_in(iv,240e6,3212e6)/2972e6)
    # download B1 over the first X seconds of its own CPU
    d=load('c2-p2a'); e=[x for x in d['events'] if x['op']=='arrive' and x['id']=='download'][0]
    for lim in [1.3e6, 5e6, 26.385e6, 1e12]:
        cur=0; bat=0; tot=0
        for s in e['program']:
            if tot>=lim: break
            if s['op']=='RUN':
                b0=cur; cur+=s['us']; tot+=s['us']; bat+=max(0,cur-10000)-max(0,b0-10000)
            elif s['op'] in ('SLEEP','WAIT','TIMER'): cur=0
        print('download first', lim/1e6, 's CPU: batch frac', round(bat/tot,3))
