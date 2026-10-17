import json,hashlib,os,sys
R='/Users/jiohin/Desktop/future-of-sw/LLM_driven_shceduling/'
def sha(p): 
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
m=json.load(open(R+'dataset/build.manifest.json'))
bad=0;n=0
for k,v in m['artifacts'].items():
    n+=1
    if sha(R+'dataset/build/'+k)!=v: bad+=1;print('MISMATCH',k)
print('core artifacts',n,'mismatch',bad)
v=json.load(open(R+'dataset/build.variants.manifest.json'))
bad=0;n=0
for k,e in v['artifacts'].items():
    n+=1
    if sha(R+'dataset/build/'+k)!=e['sha256']: bad+=1;print('MISMATCH',k)
print('variant artifacts',n,'mismatch',bad)
print(json.dumps(m['demand'],indent=0)[:3000])
