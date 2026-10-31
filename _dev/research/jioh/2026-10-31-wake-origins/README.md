# 2026-10-31 wake origins

The measured interactive applications' wakes classified by the origin of their wake chain, the data behind `_dev/docs/spec/jioh/timer-wakes-by-origin.md` (decisions 1, 8 and 9).

## Inputs

The campaigns' raw files, as released (`dataset/meas-releases.yaml`; each asset's SHA-256 checked against it on download): `perf.<phase>.timehist.txt.gz`, `perf.<phase>.wakeups.txt.gz` (`perf sched timehist -w`), the snapshots and `report.json` of every run directory. `jobs.txt` lists each run directory with the phases read and its release and asset: the phase each archetype's carried components come from — the idle phase for `office-writer` (soffice), `code-editor` (code), `mail-client` (thunderbird-send, `meas-ci:interactive:2026-09-19`'s repeats in `meas-ci-2026-09-18`) and `web-browser` (chrome); the driven phase for `image-editor` (gimp) and `video-editor` (kdenlive); the operation phase for those four operations and `mail-client`'s send (`meas-ci:interactive:2026-09-27`). Excluded run directories (`*-excluded`) are not read.

## Method

A wake is `dataset/tools/meas/campaign/analyze.py`'s: a schedule-in with a wakeup event since the thread's previous wake, the rest resumes after preemption (`merge_resumes`); the scripts import that module. The application's tree, the components (`component_name`) and the phases are as the campaign analysis reads them.

- `first_hop.py` → `first-hop.md` (with `first_hop_tables.py`): each wake by its direct waker — the X server, `swapper` (the wakeup run in interrupt context on an idle CPU), a thread of the tree, a kernel thread, another process — and the components' top wakers.
- `origins.py` → `tables.md` (with `tables.py`): each wake by the origin of its chain. The wakeup events are walked in time order; a wake by a thread of the tree, or by the X server, takes the origin of that thread's own last wake; otherwise the origin is the waker: `timer` (`swapper`), `input` (a measurement harness process — xdotool, the driver — or the driver's channel into the application, GIMP's Script-Fu server), `irq` (a kernel thread), `ext` (another process); `x` is the X server where its own wakes are not in the capture, `unknown` a tree thread not yet woken inside it, `none` a wake with no wakeup event.

Each cell is wakes/CPU: the share of the component's wakes and of its CPU.

## Results

The origin, over the whole tree (`tables.md`):

| application, phase | repeats | timer wakes/CPU | input wakes/CPU | other |
|---|---|---|---|---|
| soffice, idle | 14 | 1.00/1.00 | — | — |
| code, idle | 44 | 0.98/0.99 | — | x 0.01/0.00 |
| chrome, idle | 38 | 0.96/0.98 | — | x 0.04/0.02 |
| thunderbird-send, idle | 43 | 0.99/1.00 | — | — |
| gimp, driven | 5 | 0.27/0.05 | 0.73/0.95 | — |
| kdenlive, driven | 20 | 0.89/0.88 | 0.11/0.12 | — |
| gimp, op (unsharp mask) | 5 | 0.15/0.00 | 0.85/0.99 | irq 0.00/0.01 |
| kdenlive, op (preview render) | 20 | 0.00/0.00 | 0.99/1.00 | — |
| chrome, op (page load) | 38 | 0.35/0.27 | 0.04/0.03 | x 0.60/0.70 |
| thunderbird-send, op (send) | 8 | 0.59/0.42 | 0.40/0.58 | irq 0.01/0.01 |

By the direct waker alone (`first-hop.md`), Kdenlive's driven-phase main thread reads 0.55/0.78 woken by its own threads — `QXcbEventQueue`, the X reader, which the X server wakes in every case — and 0.45/0.22 from idle; traced to their origin, the X traffic is the X server answering the application's own timer-driven drawing, and the main thread reads timer 0.92/0.88, input 0.08/0.12. Thunderbird's idle-phase main thread is woken by Gecko's `Timer` thread for 0.54 of its wakes and 0.94 of its CPU, the `Timer` thread by `swapper`. Chromium's frame pipeline (`gpu/VizCompositorTh`, `renderer/Compositor`, `renderer/chrome`) relays a timer-started pulse between its threads. GIMP's unsharp mask read with the Script-Fu server as part of the application: timer 0.87/0.99 — the server wakes on its own poll timer before it forwards the driver's request.

## Limits

The applications were pinned to one CPU (`dataset/tools/meas/campaign/run.sh`), so a CPU-based test of interrupt against thread wake is void: a timer interrupt landing while another thread of the tree runs is credited to that thread's origin. Where the wakee sleeps, that CPU runs little else. A thread that keeps running between its wakes carries the origin of the last one, whatever else it then serves.
