import json
B='/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/coreset-single/'
def cyc(f,tid):
    d=json.load(open(B+f+'.workload.json')); e=[x for x in d['events'] if x['op']=='arrive' and x['id']==tid][0]
    return [s['us'] for s in e['program'] if s['op']=='RUN']
for f in ['c1-media','c7-media']:
    v=sorted(cyc(f,'video')); n=len(v)
    print(f,'video cycles',n,'p10',v[n//10],'p50',v[n//2],'p90',v[9*n//10],'max',v[-1], 'share >=', {th: round(sum(x>=th for x in v)/n,3) for th in [3000,5000,10000,14000]})
for f in ['c1-meeting','c7-meeting']:
    v=sorted(cyc(f,'voice')); n=len(v)
    print(f,'voice cycles',n,'p90',v[int(.9*n)],'p95',v[int(.95*n)],'p99',v[int(.99*n)],'max',v[-1],'share >=',{th: round(sum(x>=th for x in v)/n,4) for th in [10000,10001,14000]})
