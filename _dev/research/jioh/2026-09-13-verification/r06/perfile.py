import json, collections, subprocess, os, re
d=json.load(open('cachy.json')); E=d['entries']
ROOT='../sources/ananicy-rules'
files=sorted(f for f in subprocess.check_output(['git','-C',ROOT,'ls-files'],text=True).splitlines() if f.endswith('.rules'))
per=collections.defaultdict(collections.Counter)
for f,i,r in E: per[f][r.get('type','<no type>')]+=1
with open('perfile.md','w') as out:
    out.write('| # | file | entries | entries per type |\n|---|---|---|---|\n')
    for n,f in enumerate(files,1):
        c=per[f]; out.write(f"| {n} | {f} | {sum(c.values())} | {', '.join(f'{t}: {k}' for t,k in sorted(c.items(), key=lambda x:(-x[1],x[0])))} |\n")
print('files',len(files),'files with 0 entries',[f for f in files if sum(per[f].values())==0])
print('sum', sum(sum(c.values()) for c in per.values()))
# names
names=[r['name'] for f,i,r in E]
print('names ending .exe', sum(1 for n in names if n.lower().endswith('.exe')))
print('names containing / ', [n for n in names if '/' in n][:10])
print('names with space', sum(1 for n in names if ' ' in n))
# mixed-type blocks in game files
blocks=0; mixed=[]
for f in files:
    if not f.startswith('00-default/Games/'): continue
    lines=open(os.path.join(ROOT,f),encoding='utf-8').read().split('\n')
    cur=[]; head=None; start=None
    def flush():
        global blocks
        if cur:
            blocks+=1
            ts={r.get('type') for _,r in cur}
            if len(ts)>1: mixed.append((f,start,head,[(ln,r['name'],r.get('type')) for ln,r in cur]))
    for ln,l in enumerate(lines,1):
        s=l.strip()
        if s=='':
            flush(); cur=[]; head=None; continue
        if s.startswith('#'):
            if cur: flush(); cur=[]; head=None
            if head is None: head=s; start=ln
            continue
        try: r=json.loads(s)
        except: continue
        cur.append((ln,r))
    flush()
print('game blocks',blocks,'mixed-type blocks',len(mixed))
json.dump(mixed,open('mixed.json','w'),ensure_ascii=False,indent=0)
for m in mixed[:5]: print(m)
