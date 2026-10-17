import re,sys,collections
lines=open(sys.argv[1]).read().split('\n')
arch=None; group=None; comm=None; opname=None; rows=[]
for i,l in enumerate(lines,1):
    m=re.match(r'^  ([a-z][a-z0-9-]*):',l)
    if m: arch=m.group(1); group=None; comm=None; opname=None; continue
    m=re.match(r'^      ([a-z_]+):\s*(.*)$',l)
    if m:
        k=m.group(1)
        if k in('components','focus_components','operations','heavy_events'): group=k; comm=None; opname=None
        elif k in ('lifetime','binding_params','scalable','validation_stats','modeling_notes','spawned_by','spawns'): group=None
        else:
            if group not in(None,) and not l.startswith('      '+k+': {') and k not in(): pass
            # a plain param at indent 6
            if group in ('components','focus_components','heavy_events') : group=None
            if group=='operations' : group=None
            param=k
    m=re.match(r'^        ([a-z0-9-]+):\s*$',l)
    if m and group=='operations': opname=m.group(1)
    m=re.search(r'- comm: "([^"]+)"',l)
    if m: comm=m.group(1)
    s=re.search(r'source: "(meas-ci:[^"]+)"',l)
    if not s: continue
    km=re.match(r'^\s*(?:-\s*)?([a-z_]+):\s*\{',l)
    key=km.group(1) if km else None
    if key is None:  # value on the line after its key
        key=re.match(r'^\s*([a-z0-9_]+):',lines[i-2]).group(1)
    if group in ('components','focus_components','heavy_events') and key in('gap','run'):
        path=f"{arch}.{ {'components':'components','focus_components':'focus_components','heavy_events':'heavy_events'}[group]}[{comm}].{key}"
    elif group=='operations' and key in ('gap','run'):
        path=f"{arch}.operations.{opname}.components[{comm}].{key}"
    elif group=='operations' and key=='duration':
        path=f"{arch}.operations.{opname}.duration"
    else:
        path=f"{arch}.{key}"; 
    rows.append((i,path,s.group(1),group,key,arch,comm))
G={ # grounds
 'wake':'campaign/analyze.py:166-210 (wake = segment with a wakeup row; resumes merged into the wake)',
}
def classify(r):
    i,path,tag,group,key,arch,comm=r
    fam=tag.split(':')[1]
    resid = comm=='residual'
    if key=='launch':
        return 'M','desktop/launch.py:265 (analyze: the traced tree from exec to the settle\'s end), desktop/launch_fold_in.py:33-52','each pooled repeat replayed as observed (9.10 D136); no table'
    if key=='input_run':
        return 'D','campaign/analyze.py:422-428 (window rule: tree CPU from one input to the next minus idle rate x window, floored at 0)','arithmetic stated in scope (D13) except the zero floor (finding F3)'
    if key=='duration':
        return 'M','campaign/analyze.py:213-230 (trigger to done of each rc-0 operation)','wall time of the operation, as the field means'
    if key=='period':
        return 'M','campaign/pool.py:86-147 (CYCLES reference thread; cycle starts; period = mean interval)','pooled mean carried as a constant; per-repeat cycle length range in stats'
    if key=='cycle_run':
        return 'M','campaign/pool.py:120-147 (tree CPU of segments starting inside each cycle)','whole tree per cycle, as the scope says'
    if key=='tail_work':
        return 'M','background/modbuild.py:170-231; dkms results/pooled.json tail_cpu_by_comm_ms','mean of the 26 landings\' tail CPU, recomputed 10,027,983 us; not written or checked by batch_fold_in.py (finding F6)'
    if key=='dispatch_overhead':
        return 'M','build/analyze.py:418-441 (make CPU between consecutive forks of one make, pooled over every make)'+ (', via background/modbuild.py:201' if arch.startswith('module') else ''),'per fork of make, applied once per job; old X12 (mean stored as median, divided by grandchildren) gone'
    if key in('tail_run','tail_block'):
        return 'M','background/modbuild.py:211-212 -> build/shapes.py:25-35, 77-82','the serial tail (strip, zstd, depmod) as a batch loop'
    if re.search(r'_step_\d+$',key):
        if arch=='compiler-child':
            return 'M','build/shapes.py:108-133 (member CPU split at its own children\'s exits); build/analyze.py:551-562','per member and structural step; old X1 (family-member CPU bound to cc1) resolved'
        return 'M','background/modbuild.py:79-120 (fit to the kind\'s tree, fold rule) -> build/shapes.py:108-133','fold of extra processes stated in notes (9.10 D53)'
    if key.endswith('_run'):
        return 'M','build/shapes.py:25-35 (CPU from one voluntary block to the next, per thread); background/analyze.py:496-507','pooled over the program\'s threads (stated)'
    if key.endswith('_block'):
        return 'M','build/shapes.py:45-82 (program-level gap after each voluntary block, 0 if a sibling runs); background/analyze.py:508-518','program-level off-CPU time, as notes state'
    if group=='heavy_events':
        g='campaign/pool.py:78,110-117 (split_events)' if arch=='web-browser' else 'desktop/analyze.py:47 (HEAVY_EVENTS) and its split'
        return 'M',g,'runs above the stated floor (design threshold) left the component; rate = count / span'
    # components
    if fam in('interactive','playback'):
        base='campaign/analyze.py:166-210, 288-313 (role/comm component, D67); distribution.py:71-83 (gaps over merged wake times, wrapped)'
        if group=='operations': base='campaign/analyze.py:213-230 (inside operation windows), 288-313; distribution.py:71-83'
        if resid: base+='; campaign/pool.py:342-386 (residual: comms below the 95 % cut, merged)'
        note={'focus_components':'driven-phase cadence under the replayed or scripted drive','operations':'inside the operation windows laid end to end'}.get(group,'idle phase')
    elif fam=='desktop':
        if arch=='renderer-hidden':
            base='desktop/analyze.py:67-100 (per renderer process, renderers laid end to end, wrapped)'
            note='one renderer; the 12 pooled as samples'
        else:
            base='desktop/analyze.py:232 (per thread comm across the tree\'s processes, no role) -> campaign/analyze.py:166-210, 288-313'
            note='comm merged across Electron/CEF processes (finding F4 on the overview\'s wording)'
        if resid: base+='; desktop/pool.py:161 (residual)'
    elif fam=='session':
        base='session/analyze.py:153-166 (<instance>/<comm>, wakes left by cause per D27) -> campaign/analyze.py:166-210'
        note='per instance; harness/foreign causes removed (stated)'
    else:
        base='?';note='?'
    cls='M'
    if key=='gap': note='gap over merged wake times; table mean implies the carried rate (checked, <=0.12 %); '+note
    else: note='CPU per wake (resumes after preemption merged); '+note
    return cls,base,note
out=[]; cnt=collections.Counter(); bycamp=collections.Counter()
for r in rows:
    c,g,n=classify(r); cnt[c]+=1; bycamp[r[2]]+=1
    out.append(f"| `{r[1]}` | {r[0]} | `{r[2]}` | {c} | `{g}` | {n} |")
print(len(rows),cnt,len(bycamp),file=sys.stderr)
for k,v in sorted(bycamp.items()): print(k,v,file=sys.stderr)
print("\n".join(out))
