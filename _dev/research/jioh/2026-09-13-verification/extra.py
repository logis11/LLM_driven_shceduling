import json, statistics as st, glob, os, hashlib
R="/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/dataset/build/"
def L(f,m="single"): return json.load(open(f"{R}coreset-{m}/{f}.workload.json"))
def arr(d): return {e["id"]:e for e in d["events"] if e["op"]=="arrive"}
# cc1 per-child
for f in ("c1-compile","c3-workday","c6-dual"):
    a=arr(L(f)); b=a["build"]; ch=b["spawn_table"]
    cpu=[sum(s["us"] for s in c["program"] if s["op"]=="RUN") for c in ch]
    sl=[sum(s["us"] for s in c["program"] if s["op"]=="SLEEP") for c in ch]
    wall=sum(cpu)+sum(sl)+sum(s["us"] for s in b["program"] if s["op"]=="RUN")
    print(f,"children",len(ch),"cpu total",sum(cpu)/1e6,"median child cpu",st.median(cpu),"max child cpu",max(cpu),"SLEEP median",st.median(sl),"serial wall",wall/1e6, "arrive",b["t"]/1e6)
# renderer ranges
for f,pre in (("c1-office","renderers."),("c1-browsing","renderers."),("c3-workday","renderers."),("c4-compile","injected-renderers."),("c3-evening","renderers.")):
    a=arr(L(f)); rs=[e for k,e in a.items() if k.startswith(pre)]
    per=[s["period_us"] for e in rs for s in e["program"][0]["body"] if s["op"]=="TIMER"]
    run=[s["us"] for e in rs for s in e["program"][0]["body"] if s["op"]=="RUN"]
    print(f,pre,len(rs),"TIMER min/max",min(per),max(per),"RUN min/max",min(run),max(run))
# c1-office first wake
d=L("c1-office"); print("c1-office first writer wake", min(e["t"] for e in d["events"] if e["op"]=="wake" and e["target"]=="writer"))
# c3-creation last kdenlive burst end (uncontended)
d=L("c3-creation"); a=arr(d); w=sorted(e["t"] for e in d["events"] if e["op"]=="wake" and e["target"]=="video-editor")
runs=[s["us"] for s in a["video-editor"]["program"] if s["op"]=="RUN"]
print("c3-creation last wake",w[-1],"last burst",runs[-1],"ends",(w[-1]+runs[-1])/1e6)
# uncontended self-overlap: how often a wake arrives before previous burst finished (task not yet at WAIT)
def overlap(f,tid):
    d=L(f); a=arr(d); w=sorted(e["t"] for e in d["events"] if e["op"]=="wake" and e["target"]==tid)
    runs=[s["us"] for s in a[tid]["program"] if s["op"]=="RUN"]
    t_free=0; late=0
    for wt,r in zip(w,runs):
        start=max(wt,t_free)
        if t_free>wt: late+=1
        t_free=start+r
    return late,len(w),t_free/1e6, a[tid].get("depart",0)/1e6
for f,tid in (("c1-office","writer"),("c1-dev","editor"),("c1-backup","editor"),("c1-ml-train","editor"),("c2-p1a","editor"),("c7-office","writer")):
    print("uncontended self-overlap",f,tid,overlap(f,tid))
# batch C1 turnaround feasibility: work from batch arrive to 60s
for f,fg,bg in (("c1-compile","editor","build"),("c1-ml-train","editor","hog"),("c1-render","editor","bulk"),("c1-transcode","video-editor","batch"),("c1-indexing","editor","hog"),("c1-backup","editor","bulk")):
    d=L(f); a=arr(d)
    fgw=sum(s["us"] for s in a[fg]["program"] if s["op"]=="RUN")
    b=a[bg]; bw=sum(s["us"] for s in b["program"] if s["op"]=="RUN")+sum(sum(s["us"] for s in c["program"] if s["op"]=="RUN") for c in b.get("spawn_table",[]))
    avail=(60e6-b["t"])
    print(f"{f}: fg demand {fgw/1e6:.2f}s + batch CPU {bw/1e6:.2f}s = {(fgw+bw)/1e6:.2f}s vs lane time from batch arrival to 60 s {avail/1e6:.0f}s -> slack {(avail-fgw-bw)/1e6:+.2f}s")
# single vs native identical for non-game files
diff=[]
for p in sorted(glob.glob(R+"coreset-single/*.json")):
    n=p.replace("coreset-single","coreset-native")
    if open(p,"rb").read()!=open(n,"rb").read(): diff.append(os.path.basename(p))
print("single != native:",diff)
