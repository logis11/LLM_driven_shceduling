"""Every core-set timeline's per-task `source` map against the table of
_dev/research/jioh/task-9.10-scenarios-timelines/bound-values.md, entry for
entry, both directions. The expectation below transcribes that table."""
import glob, os, sys, yaml
root = sys.argv[1]
def F(s): return s.split()
UPG = F("c7-browsing c7-dev c7-gaming c7-idle c7-mail c7-media c7-meeting c7-office c7-photo c7-video-edit c2-p2b")
KB = F("c1-compile c4-compile c3-workday c6-dual")
REN = F("c1-browsing c1-office c3-workday c3-evening c4-compile c4-office c6-spoof c6-fold c7-browsing c7-office")
GAME = F("c1-gaming c4-gaming c7-gaming c2-p2a c2-p2b c3-evening c6-dual")
exp = {}  # (file, archetype, key) -> (value, tags)
def add(files, arch, key, value, tags):
    for f in files: exp[(f, arch, key)] = (value, tuple(tags) if isinstance(tags, list) else (tags,))
add(UPG, 'package-upgrade', 'total_work', '26.385s', 'meas-ci:background:2026-10-01')
add(F("c1-indexing c7-indexing c2-p1b"), 'file-indexer', 'total_work', '39.435s', 'meas-ci:background:2026-10-02b')
add(F("c1-ml-train c7-ml-train c2-p1a"), 'cpu-batch', 'total_work', '1389.885s', 'meas-ci:background:2026-10-03')
add(F("c1-ml-train c7-ml-train c2-p1a"), 'cpu-batch', 'program', 'python3', ['pytorch-examples', 'meas-ci:background:2026-10-03'])
add(F("c1-transcode c7-transcode c3-creation"), 'video-transcoder', 'total_work', '2970.871s', 'meas-ci:background:2026-10-03b')
add(F("c1-render c7-render c2-p3a"), 'cpu-batch', 'total_work', '16.545s', 'meas-ci:background:2026-10-03c')
add(F("c1-render c7-render c2-p3a"), 'cpu-batch', 'program', 'kdenlive_render', ['kdenlive', 'meas-ci:background:2026-10-03c'])
add(F("c1-backup c7-backup c2-p3b"), 'incremental-backup', 'total_work', '165.668s', 'meas-ci:background:2026-10-04')
add(F("c2-p2a c2-p2a-idle"), 'game-download', 'total_work', '727.170s', 'meas-ci:background:2026-09-19')  # c2-p2a-idle: derived, inherits
exp[('c2-p2a-idle', 'game-download-idle', 'total_work')] = exp.pop(('c2-p2a-idle', 'game-download', 'total_work'))
add(KB, 'build-orchestrator', 'spawn_count', 2908, 'meas-ci:build:2026-09-18')
add(KB, 'build-orchestrator', 'child_name', 'cc1', 'meas-ci:build:2026-09-18')
add(['c7-compile'], 'module-build-orchestrator', 'child_name', 'cc1', 'meas-ci:background:2026-10-02')
add(REN, 'renderer-hidden', 'count', 4, ['glam', 'meas-ci:desktop:2026-10-04'])
add(GAME, 'game-task-chain', 'member_names', None, 'lavd-ossna24:s16')
add(KB, 'build-orchestrator', 'parallelism_cap', 8, 'design')
add(['c7-compile'], 'module-build-orchestrator', 'parallelism_cap', 8, 'design')
for f, ls in [('c1-gaming', .9), ('c4-gaming', .9), ('c7-gaming', .9), ('c2-p2a', .95), ('c2-p2a-idle', .95), ('c2-p2b', .95), ('c3-evening', 1.45), ('c6-dual', .6)]:
    exp[(f, 'game-task-chain', 'lane_share')] = (ls, ('design',))
add(['c6-spoof'], 'cpu-batch', 'total_work', '30s', 'design')
add(['c6-spoof'], 'cpu-batch', 'program', 'spoof', 'design')
add(['c4-office'], 'file-archiver', 'total_work', '6s', 'design')
got = {}
for p in sorted(glob.glob(os.path.join(root, 'dataset/timelines/coreset/*.timeline.yaml'))):
    fid = os.path.basename(p)[:-len('.timeline.yaml')]
    t = yaml.safe_load(open(p))
    for task in t.get('tasks') or []:
        src = task.get('source') or {}
        bind = task.get('bind') or {}
        for k, tags in src.items():
            tags = tuple(tags) if isinstance(tags, list) else (tags,)
            v = bind.get(k, task.get(k))
            key = (fid, task['archetype'], k)
            if key in got and got[key][1] != tags:
                print('MULTI', key, got[key], tags)
            got[key] = (v, tags)
        # bound values without a source entry
        for k in list(bind) + [x for x in ('count',) if x in task]:
            if k not in src:
                print('BOUND, NO SOURCE', fid, task['id'], k)
bad = 0
for k in sorted(set(exp) | set(got), key=str):
    e, g = exp.get(k), got.get(k)
    if e is None: print('IN TIMELINE, NOT IN TABLE', k, g); bad += 1; continue
    if g is None: print('IN TABLE, NOT IN TIMELINE', k, e); bad += 1; continue
    if e[1] != g[1]: print('TAG DIFFERS', k, 'table', e[1], 'timeline', g[1]); bad += 1
    elif e[0] is not None and str(e[0]) != str(g[0]): print('VALUE DIFFERS', k, 'table', e[0], 'timeline', g[0]); bad += 1
print(f'entries: table {len(exp)}, timelines {len(got)}, disagreements {bad}')
