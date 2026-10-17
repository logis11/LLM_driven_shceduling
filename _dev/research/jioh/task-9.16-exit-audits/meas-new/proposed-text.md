# 9.16 — proposed text from the two new computations

For the lead to apply, in 9.16's order (spec decision 4: code and data first, at most one rebuild, then docs and memos). Every number rests on `out/burstiness-tables.md`, `out/windows-tables.md` and `out/stability-ledger-output.md` beside this page (`burstiness.md`, `stability-ledger.md` read them).

## Code and data

### C1. `burstiness.py` and `windows.py` find `video-editor`'s idle landings

The idle campaign's artifacts are `meas-interactive-kdenlive-r<k>-idle`; both tools look the idle repeats up as `…-full` and stop ("kdenlive repeat 1 of run 37273046929: 0 artifacts").

`dataset/tools/meas/control_report.py`, after `IDLE_FROM_95`:

```python
# the mode the idle campaign's artifacts are named by (9.10 kdenlive-idle method §1: `meas-interactive-kdenlive-r<k>-idle`)
IDLE_MODE_95 = {"kdenlive": "idle"}
```

`dataset/tools/meas/burstiness.py`: `campaign_streams(app, pooled, root, phase="idle", mode="full")` passes `mode` to `artifact_dir`; `campaign_entries` calls it with `mode=cr.IDLE_MODE_95.get(app, "full")`.

`dataset/tools/meas/windows.py`, `campaign_entries`, the `PHASES_95` loop: `b.artifact_dir(root, app, rep, run["run_id"][str(rep)], cr.IDLE_MODE_95.get(app, "full") if phase == "idle" else "full")`.

`test_meas_burstiness.py` / `test_meas_windows.py` may want a case for the idle mode.

### C2. `renderer-hidden`'s scope: the residual's window reading

`dataset/tools/meas/desktop/fold_in.py`, `WINDOWS_1005B["renderer-hidden"]` — replace

> the residual (`MemoryInfra`, `ThreadPoolServi`) wakes at 3.6 times its phase rate in the first 100 s and 2.4 times 400–500 s in;

with

> the residual (`MemoryInfra`, `ThreadPoolServi`) wakes at 1.5 times its phase rate in the first 100 s and 1.4 times 400–500 s in, every `MemoryInfra` wake falling in those two windows;

then regenerate the entry with the desktop fold-in, which rewrites `dataset/archetypes.yaml`'s `renderer-hidden` scope (a compile input: this falls in 9.16's one rebuild). The 3.6 and 2.4 are `MemoryInfra` alone (27 and 18 of its 45 wakes over the 5 repeats, against 7.5 a window on average); the library's residual also holds `ThreadPoolServi`, 300 wakes spread over every window. The same statement stands in 9.10 D156 and `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/results.md`; the correction is 9.16's record to make.

### C3. The ledger script, committed

Move `stability_ledger.py` to `dataset/tools/meas/stability_ledger.py` (it finds the repository root by walking up to the nearest `dataset/tools`, so it runs unchanged from there; its output does not depend on the working directory — checked by a run from `/tmp`) and add a row to `dataset/tools/meas/README.md`'s tool table, after `stopping.py`:

> | `stability_ledger.py` | pool | the stability ledger over the pooled records the library is folded from: the values that met the tolerance, those carried under each exception class, the largest half-width carried |

If it stays in 9.16's research folder instead, the citations below name `_dev/research/jioh/task-9.16-exit-audits/meas-new/stability_ledger.py`.

## `docs/workload/measurement-overview.md`

### O1. §8 "Compile fidelity" — the threat sentence

Replace

> The dispersion ratio, measured over compiled, median over the carried repeats (`dataset/tools/meas/burstiness.py`, read 2026-09-27): `chat-client` 3.3–11×, `code-editor` 2.6–3.4×, `web-browser` 2.8–3.4×, `mail-client` 1.9–3.0×, `game-client` 1.9–3.0×, `video-editor` 1.3–1.4×, `renderer-hidden` 1.06–1.15×; about 1 for `audio-server`, `service-manager` and `message-bus`; below 1, the compiled stream the burstier, for `compositor-shell` (0.86–0.97) and `office-writer` (0.60–0.91). `video-editor`'s figure was read on its idle phase of `meas-ci:interactive:2026-09-18` and `renderer-hidden`'s on `meas-ci:desktop:2026-09-20`; their current pools, `meas-ci:interactive:2026-10-05` and `meas-ci:desktop:2026-10-05b`, are not yet read.

with

> The dispersion ratio, measured over compiled, median over the carried repeats (`dataset/tools/meas/burstiness.py`, read 2026-09-27; `renderer-hidden` on `meas-ci:desktop:2026-10-05b` and `video-editor`'s idle phase on `meas-ci:interactive:2026-10-05`, read 2026-10-17): `chat-client` 3.3–11×, `code-editor` 2.6–3.4×, `web-browser` 2.8–3.4×, `mail-client` 1.9–3.0×, `game-client` 1.9–3.0×, `renderer-hidden` 1.26–1.44×, `video-editor` 1.22–1.32×; about 1 for `audio-server`, `service-manager` and `message-bus`; below 1, the compiled stream the burstier, for `compositor-shell` (0.86–0.97) and `office-writer` (0.60–0.91).

### O2. §8 "Time windows" — the exception closed

Delete the bullet's last two sentences:

> `video-editor`'s idle phase is the exception: it was read on `meas-ci:interactive:2026-09-18`, and its current pool, `meas-ci:interactive:2026-10-05`, is not yet read.

(Read 2026-10-17 over nine 20 s windows: each window's wake rate 0.95–1.09 times the phase's, no part of the phase holding work the rest does not, so no scope statement follows; the bullet's general sentence then covers every carried phase.)

### O3. §7 — the 1 µs floor sentence

Replace

> Values of a few microseconds pass by the 1 µs floor rather than the 5 %: the block per run of `file-archiver`, `game-download`, `package-upgrade`, `video-transcoder` and `incremental-backup`, `kdenlive_render`'s in `cpu-batch`, the Steam client's `CJobMgr::m_Work` run mean.

with

> Values of a few microseconds pass by the 1 µs floor rather than the 5 %: the block per run of `file-archiver`, `game-download`, `package-upgrade`, `video-transcoder` and `incremental-backup`, `kdenlive_render`'s in `cpu-batch`, the Steam client's `CJobMgr::m_Work` and `ThreadPoolForeg` run means, and `mail-client`'s `SwComposite` run mean in the send operation.

### O4. §7 — the ledger, a closing paragraph after the paragraph ending "(the RQ0 gate spec's statement `re-measurement-contingency`)."

> **The ledger** (`dataset/tools/meas/stability_ledger.py`, read 2026-10-17), over the pooled records the 28 measured entries are folded from, each value counted from the record its entry takes it from. Their stability lists hold 406 values, 4 of them the stimulus-sensitivity check's per-input means under 136M (§8), on the lists but not carried. 369 met the tolerance, 9 of them by the 1 µs floor. 37 are carried under a class: 15 vary between sessions, 10 under recording runs out, 9 under spread follows the machine, 3 under sparse component; the 2 rare events, `web-browser`'s `MemoryInfra` pass and `game-client`'s HTTP burst, are carried beside the rule. No value that fails the rule is carried without a class. The largest half-width carried is ±61.3 %, `renderer-hidden`'s residual run mean (sparse component, 5 repeats); under the other classes the widest are ±27.3 % (`cpu-batch`'s `python3` runs between blocks, machine), ±18.4 % (`mail-client`'s send `StreamTrans` run mean, recording runs out) and ±17.6 % (`renderer-hidden`'s `Compositor` and `PerfettoTrace` wake rates, between sessions). Among the values that met the tolerance the widest is `file-archiver`'s block per run, ±40.5 % (a half-width of 0.065 µs, inside the floor).

Bump `Updated` (already 2026-10-17).

## `docs/memos/2026-09-20-dataset-validity-review.md` — the open line

Replace line 4

> Open — §3's ask, the stability-ledger summary (the quantities that met the tolerance, those carried under each exception class, the largest half-width carried), to be computed by a script over the slices' pooled records and published in `docs/workload/measurement-overview.md`'s stability sections, with 9.16's measurement audit (`_dev/TODO.md`); owner 인지오. §4's ask is answered by 9.14 decision 4, …

with

> Closed — §3's ask is answered by the stability ledger in `docs/workload/measurement-overview.md` §7, computed by `dataset/tools/meas/stability_ledger.py` over the pooled records the library is folded from (2026-10-17): of 406 values on the stability lists, 369 met the tolerance and 37 are carried under a stated exception, with two rare events carried beside the rule; the largest half-width carried is ±61.3 %, `renderer-hidden`'s residual run mean. §4's ask is answered by 9.14 decision 4, …

(the rest of the line unchanged). `Updated` is already 2026-10-17.

## `docs/README.md`

- Line 98 (the reading-path entry for the validity memo): replace "Open: §3's stability-ledger summary, computed over the slices' pooled records and published in the measurement overview with 9.16's measurement audit; owner 인지오" with "Closed: §3's stability ledger is in the measurement overview §7".
- Line 148 (the index table): "memo (open)" → "memo (closed)".

## The dataset guidebook

### G1. Volume 2, `docs/guidebook/dataset/02-the-archetype-library.md` line 1501

Replace

> `video-editor`(1.3–1.4배)와 `renderer-hidden`(1.06–1.15배)은 차이가 작고(둘 다 지금 실린 pool이 아니라 그때의 campaign에서 읽은 값),

with

> `renderer-hidden`(1.26–1.44배)과 `video-editor`(1.22–1.32배)는 차이가 작고(둘 다 지금 실린 pool, `meas-ci:desktop:2026-10-05b`와 `meas-ci:interactive:2026-10-05`의 유휴 단계에서 2026-10-17에 다시 읽은 값),

### G2. Volume 6, `docs/guidebook/dataset/06-grounding-measurement-verification.md` line 1039

Replace "`video-editor` 1.3–1.4배, `renderer-hidden` 1.06–1.15배 더 몰려 있고" with "`renderer-hidden` 1.26–1.44배, `video-editor` 1.22–1.32배 더 몰려 있고", and replace

> `video-editor`의 값은 `meas-ci:interactive:2026-09-18`의 유휴 단계에서, `renderer-hidden`의 값은 `meas-ci:desktop:2026-09-20`에서 읽은 것이고, 두 entry가 지금 담은 pool(`meas-ci:interactive:2026-10-05`, `meas-ci:desktop:2026-10-05b`)은 아직 읽지 않았습니다. 그 다시 읽기는 9.16의 측정 감사에 들어 있습니다(`_dev/TODO.md` 9.16 줄).

with

> `renderer-hidden`과 `video-editor`의 값은 두 entry가 지금 담은 pool(`meas-ci:desktop:2026-10-05b`, `meas-ci:interactive:2026-10-05`의 유휴 단계)에서 2026-10-17에 다시 읽은 것입니다.

### G3. Volume 6 line 1554 — the ledger now exists

Replace from "라이브러리 전체의 요약 수치(…)를 한곳에 모은 표는 아직 없습니다." to the end of the item with

> 라이브러리 전체의 요약 수치는 `measurement-overview.md` §7의 ledger 단락에 있습니다(`dataset/tools/meas/stability_ledger.py`, 2026-10-17). 28개 측정 entry가 접혀 나온 pooled record의 stability 목록에 값이 406개 있고(그중 4개는 136M 자극 민감도 점검의 입력당 평균으로, 목록에는 있지만 싣지 않음), 369개가 허용 오차를 통과했으며(9개는 1 µs 바닥으로), 37개가 예외 class로 실렸습니다(session 사이에서 변함 15, 녹화가 끝남 10, machine 따라 흩어짐 9, 드문 component 3). 드문 사건 2개는 규칙 밖에서 따로 실렸습니다. 실린 가장 넓은 반폭은 ±61.3 %, `renderer-hidden`의 residual run 평균입니다.

The 9.16 hand-off lists in volume 6 (lines 1672–1673) and volume 8 (line 1801) name these two items as pending; they close with the rest of 9.16's list when the lead writes the exit record.
