# Ideal-machine model of interbench e612a65 periodic_schedule()+emulate_x() (zero latency, exact burns/sleeps)
t=0; st=dict(met=0,missed=0,ach=0,mb=0,n=0,lat=0)
def ps(run,interval,deadline):
    global t
    lat=0
    if t>deadline: lat=t-deadline
    ml=0
    if interval and t>deadline+interval:
        deadline+=interval; k=(t-deadline)//interval+1
        st['missed']+=k; ml=k*interval; deadline+=k*interval; st['mb']+=k
        t=deadline; st['lat']+=lat+ml; st['n']+=1; return deadline
    t+=run; st['ach']+=1; busy.append(run)
    deadline+=interval
    if deadline>=t: st['met']+=1
    else:
        if interval:
            k=(t-deadline)//interval+1; st['missed']+=k; ml=k*interval; deadline+=k*interval
            if k>1: st['mb']+=k
        else:
            deadline=t; st['lat']+=lat+ml; st['n']+=1; return deadline
    t=max(t,deadline)
    st['lat']+=lat+ml; st['n']+=1; return deadline
busy=[]
d=0; t0=0
for cycle in range(3):
    start=t
    for i in range(101):
        d=ps(i*1000,(100-i)*1000,d); d+=i*1000
    print('cycle',cycle,'wall ms',(t-start)/1000,'cpu ms',sum(busy)/1000); busy=[]
print(st, 'deadlines met %', 100*st['met']/(st['met']+st['missed']), 'desired cpu %', 100*st['ach']/(st['ach']+st['mb']))
