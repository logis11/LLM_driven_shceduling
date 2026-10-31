# 2026-10-31 wake origins

The measured interactive applications' wakes classified by the origin of their wake chain, the data behind `_dev/docs/spec/jioh/timer-wakes-by-origin.md` (decisions 1, 8 and 9).

## Inputs

The campaigns' raw files, as released (`dataset/meas-releases.yaml`; each asset's SHA-256 checked against it on download): `perf.<phase>.timehist.txt.gz`, `perf.<phase>.wakeups.txt.gz` (`perf sched timehist -w`), the snapshots and `report.json` of every run directory. `jobs.txt` lists each run directory with the phases read and its release and asset: the phase each archetype's carried components come from — the idle phase for `office-writer` (soffice), `code-editor` (code), `mail-client` (thunderbird-send, `meas-ci:interactive:2026-09-19`'s repeats in `meas-ci-2026-09-18`) and `web-browser` (chrome); the driven phase for `image-editor` (gimp) and `video-editor` (kdenlive); the operation phase for those four operations and `mail-client`'s send (`meas-ci:interactive:2026-09-27`). Excluded run directories (`*-excluded`) are not read.

## Method

A wake is `dataset/tools/meas/campaign/analyze.py`'s: a schedule-in with a wakeup event since the thread's previous wake, the rest resumes after preemption (`merge_resumes`); the scripts import that module. The application's tree, the components (`component_name`) and the phases are as the campaign analysis reads them.

- `first_hop.py` → `first-hop.md` (with `first_hop_tables.py`): each wake by its direct waker — the X server, `swapper` (the wakeup run in interrupt context on an idle CPU), a thread of the tree, a kernel thread, another process — and the components' top wakers.
- `origins.py` → `tables.md` (with `tables.py`): each wake by the origin of its chain. The wakeup events are walked in time order; a wake by a thread of the tree, or by the X server, takes the origin of that thread's own last wake, the X server's wakes walked whether or not the snapshots hold it (Chrome's and VS Code's do not); otherwise the origin is the waker: `timer` (`swapper`), `input` (a measurement harness process — xdotool, the driver — or the driver's channel into the application, GIMP's Script-Fu server), `irq` (a kernel thread), `ext` (another process); `x` is the X server where its own wakes are not in the capture, `unknown` a tree thread not yet woken inside it, `none` a wake with no wakeup event.
- `within_event.py` (the interactive campaigns, `campaign/analyze.py`'s wakes) and `within_event_desktop.py` (a desktop subject, `desktop/analyze.py`'s): 9.5 D57's test on a pool's parts — the part's wake rate over a window of the campaign's phase length slid along a long-phase probe, against its spread across the pool's repeats.

Each cell is wakes/CPU: the share of the component's wakes and of its CPU.

## Results

The origin, over the whole tree (`tables.md`):

| application, phase | repeats | timer wakes/CPU | input wakes/CPU | other |
|---|---|---|---|---|
| soffice, idle | 14 | 1.00/1.00 | — | — |
| code, idle | 44 | 0.99/1.00 | — | — |
| chrome, idle | 38 | 1.00/1.00 | — | — |
| thunderbird-send, idle | 43 | 0.99/1.00 | — | — |
| gimp, driven | 5 | 0.27/0.05 | 0.73/0.95 | — |
| kdenlive, driven | 20 | 0.89/0.88 | 0.11/0.12 | — |
| gimp, op (unsharp mask) | 5 | 0.15/0.00 | 0.85/0.99 | irq 0.00/0.01 |
| kdenlive, op (preview render) | 20 | 0.00/0.00 | 0.99/1.00 | — |
| chrome, op (page load) | 38 | 0.36/0.27 | 0.64/0.73 | — |
| thunderbird-send, op (send) | 8 | 0.59/0.42 | 0.40/0.58 | irq 0.01/0.01 |

By the direct waker alone (`first-hop.md`), Kdenlive's driven-phase main thread reads 0.55/0.78 woken by its own threads — `QXcbEventQueue`, the X reader, which the X server wakes in every case — and 0.45/0.22 from idle; traced to their origin, the X traffic is the X server answering the application's own timer-driven drawing, and the main thread reads timer 0.92/0.88, input 0.08/0.12. Thunderbird's idle-phase main thread is woken by Gecko's `Timer` thread for 0.54 of its wakes and 0.94 of its CPU, the `Timer` thread by `swapper`. Chromium's frame pipeline (`gpu/VizCompositorTh`, `renderer/Compositor`, `renderer/chrome`) relays a timer-started pulse between its threads. GIMP's unsharp mask read with the Script-Fu server as part of the application: timer 0.87/0.99 — the server wakes on its own poll timer before it forwards the driver's request.

## The split pools against the stability rule

Re-pooled with the split (the coverage cut per channel) and the X server walked whatever the snapshots hold, the parts that fail the stability rule at the repeats obtained, with 9.5 D57's test on the long-phase probes: the part's wake rate over the campaign's phase length, slid along the probe's phase past the campaign's settle, against its spread across the repeats; both half the range over the midpoint. `within_event.py` reads the interactive campaigns' probes, `within_event_desktop.py` the Steam client's, `dataset/tools/meas/session/within_run.py` the session's.

| application, phase | part | wakes a phase | within one run | across the repeats | probe |
|---|---|---|---|---|---|
| code, idle, 44 repeats | `renderer/code [event]` | 29–71 | ±31.6 % | ±42.0 % | D52, from 200 s, 700 s windows every 10 s |
| code | `gpu/VizCompositorTh [event]` | 12–43 | ±26.1 % | ±56.4 % | the same |
| code | `renderer/Compositor [event]` | 10–57 | ±48.7 % | ±70.1 % | the same |
| code | `gpu/Chrome_ChildIOT [event]` | 9–39 | ±29.4 % | ±62.5 % | the same |
| code | `residual [event]` | 10–35 | ±36.0 % | ±55.6 % | the same |
| chrome, idle, 38 repeats | `renderer/Compositor [event]` | 2–22 | ±66.7 % | ±83.3 % | D50 (35494199119), from 240 s, 600 s windows every 10 s |
| chrome | `gpu/VizCompositorTh [event]` | 2–22 | ±57.9 % | ±83.3 % | the same |
| chrome | `utility/ThreadPoolForeg [event]` | 2–9 | 0–8 wakes a window | ±63.6 % | the same |
| thunderbird-send, idle, 77 repeats | `BgIOThr~Pool [event]` (run mean) | 2–3 | two wakes in every window | ±20.0 % | 35436084336, from 360 s, 600 s windows every 10 s |
| steam, shown, 12 repeats | `steam [event]` | 31–104 | ±79.3 % | ±54.1 % | the 9.8 probe, 600 s windows every 60 s |
| steam | `steamwebhelper [event]` | 36–112 | ±63.2 % | ±51.4 % | the same |
| steam | `CJobMgr::m_Work [event]` | 41–62 | ±35.8 % | ±20.4 % | the same |
| steam | `Compositor [event]` | 2–37 | ±32.2 % | ±89.7 % | the same |
| steam | `Chrome_ChildIOT [event]` | 6–22 | ±86.9 % | ±57.1 % | the same |
| steam | `residual [event]` | 24–143 | ±87.6 % | ±71.3 % | the same |
| session, steady, 24 repeats | `wireplumber/gmain` (timer part) | 8–16 | ±15.4–15.9 % | ±36.8 % | probes 36, 41, 44, 1800 s windows every 60 s |
| session | `pid1/systemd [event]` (run mean) | 114–133 | ±18.4–20.4 % | ±29.2 % | the same |
| session | `system-bus/dbus-daemon [event]` | 16–36 | ±25.1–28.4 % | ±40.5 % | the same |

`pid1/systemd` and `system-bus/dbus-daemon` are 99.4 % and 98.3 % event-caused, so their parts carry the components' whole wakes. Before the X server was walked for Chrome and VS Code, whose snapshots hold no X server, code's `gpu/VizCompositorTh [event]` woke 1.22 times a second and moved ±4.1 % within a run against ±49.4 % across; read through the X server it is 0.036 a second.

Kdenlive's driven phase: the main thread's timer part's run mean ±5.35 % over 20 repeats (±5.00 % before the split); across the repeats the run means of the phase's other four carried parts move with it, correlation +0.80 to +0.94.

## Limits

The applications were pinned to one CPU (`dataset/tools/meas/campaign/run.sh`), so a CPU-based test of interrupt against thread wake is void: a timer interrupt landing while another thread of the tree runs is credited to that thread's origin. Where the wakee sleeps, that CPU runs little else. A thread that keeps running between its wakes carries the origin of the last one, whatever else it then serves.
