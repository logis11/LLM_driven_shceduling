# Venue mix per timeline: every archetype a timeline binds (plus the spawned
# child entries its orchestrators carry), mapped to its category_source.
import re, sys, yaml, glob, os, collections
root = sys.argv[1]
arch = yaml.safe_load(open(os.path.join(root, 'dataset/archetypes.yaml')))
arch = arch.get('archetypes', arch)
arch = {k: v for k, v in arch.items() if isinstance(v, dict)}
cs = {k: v.get('category_source') for k, v in arch.items()}
CHILD = {'build-orchestrator': 'compiler-child', 'module-build-orchestrator': 'module-compiler-child'}
def venue(a): return 'runner' if cs[a] == 'meas' else cs[a]
core, gen = [], collections.Counter()
for d in sorted(glob.glob(os.path.join(root, 'dataset/timelines/coreset/*.timeline.yaml'))) + sorted(glob.glob(os.path.join(root, 'dataset/generated/*/*.timeline.yaml'))):
    if '/coreset/' in d:
        t = yaml.safe_load(open(d))
        archs = {task['archetype'] for task in (t.get('tasks') or []) if task.get('archetype')}
    else:  # generated files: token read, comments stripped (pure-Python YAML is slow over 1,571 files)
        txt = '\n'.join(l.split('#', 1)[0] for l in open(d))
        archs = set(re.findall(r'archetype:\s*([a-z0-9-]+)', txt))
    archs |= {CHILD[a] for a in archs if a in CHILD}
    unknown = sorted(a for a in archs if a not in cs)
    v = ' + '.join(sorted({venue(a) for a in archs if a in cs}))
    rel = os.path.relpath(d, root)
    if '/coreset/' in rel:
        core.append((os.path.basename(rel)[:-len('.timeline.yaml')], sorted(archs), v, unknown))
    else:
        gen[(rel.split('/')[2], v, tuple(unknown))] += 1
print("library:", collections.Counter(cs.values()))
for n, a, v, u in core:
    print(f"| `{n}` | {', '.join(a)} | {v} |{' UNKNOWN '+str(u) if u else ''}")
print()
for k, n in sorted(gen.items()): print(k, n)
