"""Per scored ready_wait term of the scoring spec: the compiled file's wake
events on the term's entity and channel kind inside the term's window
(offered wakes, read on dataset/build/coreset-single). Also verifies each
file read against the core manifest's sha256 first."""
import hashlib, json, sys, yaml, pathlib
root = pathlib.Path(sys.argv[1])
man = json.load(open(root / 'dataset/build.manifest.json'))['artifacts']
spec = yaml.safe_load(open(root / 'harness/scoring/scoring-spec.yaml'))
judging = set(yaml.safe_load(open(root / 'harness/experiments/rq0-gate.yaml'))['files']['judging'])
for wid, f in sorted(spec['files'].items()):
    terms = [t for t in (f or {}).get('terms') or [] if t['metric'] == 'ready_wait']
    if not terms:
        continue
    rel = f'coreset-single/{wid}.workload.json'
    raw = (root / 'dataset/build' / rel).read_bytes()
    ok = hashlib.sha256(raw).hexdigest() == man[rel]
    ev = json.loads(raw)['events']
    for t in terms:
        w = t.get('window') or {}
        s, e = w.get('start_us', 0), w.get('end_us', float('inf'))
        n = sum(1 for x in ev if x['op'] == 'wake' and x['target'] == t['entity']
                and x['channel'].split(':')[0] == t.get('channel') and s <= x['t'] < e)
        print(f"| `{wid}` | {'judging' if wid in judging else 'reporting'} | `{t['entity']}` | {t.get('channel')} | {w.get('start_us','')}–{w.get('end_us','')} | {n} | {'ok' if ok else 'HASH MISMATCH'} |")
