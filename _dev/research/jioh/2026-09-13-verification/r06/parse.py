import json, sys, subprocess, collections, os
ROOT = sys.argv[1]
OUT = os.path.abspath(sys.argv[2])
os.chdir(ROOT)
files = subprocess.check_output(['git','ls-files','-z'],text=True).split('\0')
rules = sorted(f for f in files if f.endswith('.rules'))
types_files = sorted(f for f in files if f.endswith('.types'))
SCHEMA_KEYS = {"nice","latency_nice","ionice","sched","rtprio","ioclass","oom_score_adj","cpuset","cgroup","type"}
types = {}
for tf in types_files:
    for i,l in enumerate(open(tf,encoding='utf-8'),1):
        s=l.strip()
        if not s or s.startswith('#'): continue
        r=json.loads(s); types[r['type']]=(tf,i,r)
entries=[]; malformed=[]; other=[]
for f in rules:
    for i,l in enumerate(open(f,encoding='utf-8',newline=''),1):
        raw=l.rstrip('\n')
        s=raw.strip()
        if s=='' : continue
        if s.startswith('#'):
            if not raw.startswith('#'): other.append((f,i,'comment with leading whitespace',raw))
            continue
        if raw.endswith('\r'): other.append((f,i,'CRLF',raw))
        try:
            r=json.loads(s)
        except Exception as e:
            malformed.append((f,i,'JSON: '+str(e),raw)); continue
        if not isinstance(r,dict):
            malformed.append((f,i,'not object',raw)); continue
        bad=set(r)-SCHEMA_KEYS-{'name'}
        if bad: malformed.append((f,i,'unknown keys %s'%sorted(bad),raw))
        if 'name' not in r: malformed.append((f,i,'no name',raw))
        if raw!=raw.lstrip(): other.append((f,i,'leading whitespace',raw))
        entries.append((f,i,r))
json.dump({'types':{k:[v[0],v[1],v[2]] for k,v in types.items()},'entries':entries,'malformed':malformed,'other':other},open(OUT,'w'),ensure_ascii=False)
print('rules files',len(rules)); print('types defined',len(types),list(types))
print('rule entries (parsed JSON objects)',len(entries))
print('malformed',len(malformed))
for m in malformed: print('  ',m)
print('other oddities',len(other))
for m in other[:30]: print('  ',m)
