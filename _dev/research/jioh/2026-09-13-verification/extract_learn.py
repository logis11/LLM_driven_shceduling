import re,html,sys
def extract(path):
    t=open(path,encoding='utf-8').read()
    meta=dict(re.findall(r'<meta name="([^"]*)" content="([^"]*)"',t))
    m=re.search(r'<main.*?</main>',t,re.S); body=m.group(0) if m else t
    body=re.sub(r'<(script|style)[^>]*>.*?</\1>','',body,flags=re.S)
    body=re.sub(r'</?(p|div|h[1-6]|li|tr|pre|br|table|ul|ol|section|blockquote)[^>]*>','\n',body)
    body=re.sub(r'<[^>]+>','',body)
    body=html.unescape(body)
    lines=[re.sub(r'[ \t]+',' ',l).strip() for l in body.split('\n')]
    out=[]
    for l in lines:
        if l or (out and out[-1]): out.append(l)
    hdr='\n'.join(f'# meta {k}: {meta[k]}' for k in ['ms.date','updated_at','git_commit_id','original_content_git_url','original_ref_skeleton_git_url','ms.topic'] if k in meta)
    return hdr+'\n\n'+'\n'.join(out)
for p in sys.argv[1:]:
    open(p.rsplit('.',1)[0]+'.txt','w').write(extract(p))
