# php-fpm census — the 9.5–9.8 campaigns' wakes traced to their causes

The census 9.9 D27 handed to 9.16 ("the campaigns of 9.5–9.8 ran on the same runner image, beside the same `php-fpm` and their own workflow loops … Their released wakeup rows allow the same census"; `_dev/research/jioh/task-9.9-daemons-session/changelog.md`, end of D27), run 2026-10-20. D27 traced every wake of a session entry's thread to its cause through the trace and took out of the components the wakes whose cause lies outside the observed desktop — a package Ubuntu 24.04's desktop manifest does not hold (`php8.3-fpm`, PHP's session cleanup in `php-common`, `podman`, `sphinxsearch`), the harness; D32 and D37 added a desktop unit that a stock install leaves inactive and the runner image runs (`systemd-networkd`); D47 reverted D32's sysstat ground. This record applies the same tracing to every carried value of 9.5–9.8 that counts wakes or sums their runs, and reads how far each value would move without those wakes. No dataset value, tool, doc or guidebook was changed.

`<scratch>` is `/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad/phpfpm`; the downloaded releases are in `<scratch>/rel/`, the census outputs in `<scratch>/out/` (not committed: `tb-send.json` alone is 142 MB).

## What ran

| campaign (tag) | release | entries and carried phase | repeats traced |
|---|---|---|---|
| `meas-ci:interactive:2026-09-18` | `meas-ci-2026-09-18` | `office-writer` idle components and driven `input_run`; `image-editor` driven `focus_components` and `unsharp-mask` operation; `video-editor` driven `focus_components` and `preview-render` operation | 14, 5, 20 |
| `meas-ci:interactive:2026-09-19` | `meas-ci-2026-09-18` (43) + `meas-ci-2026-09-28` (34) | `mail-client` idle components | 77 |
| `meas-ci:interactive:2026-09-20` | `meas-ci-2026-09-20` | `web-browser` idle components, `page-load` operation, driven `input_run` | 38 |
| `meas-ci:interactive:2026-09-25` | `meas-ci-2026-09-25` | `code-editor` idle components (from 200 s, 9.5 D83), driven `input_run` | 44 (43 driven) |
| `meas-ci:interactive:2026-09-27` | `meas-ci-2026-09-27` | `mail-client` `send` operation, driven `input_run` | 8 |
| `meas-ci:playback:2026-09-18` | `meas-ci-2026-09-18` | `video-player`, `audio-player` play phase (`period`, `cycle_run`) | 24, 31 |
| `meas-ci:playback:2026-09-20` | `meas-ci-2026-09-20` | `video-call` play phase | 45 |
| `meas-ci:build:2026-09-18` | `meas-ci-build-2026-09-18` | `compiler-child` member steps and `build-orchestrator` dispatch run, warm `make -j8` | 14 |
| `meas-ci:background:2026-09-19` | `meas-ci-background-2026-09-19` | `file-archiver` (7-Zip, `7z-mmt8-warm`); `game-download` and `game-download-idle`, which shares its tables (SteamCMD, `steam-fresh-shaped`) | 6, 30 |
| `meas-ci:desktop:2026-09-20` | `meas-ci-desktop-2026-09-20` | `chat-client` (Element, idle); `game-client` (Steam, shown) | 18, 12 |

Each repeat was read exactly as its family's committed pool reads it — `campaign/analyze.analyze_run` at the pool's settings with the operation windows and heavy events of `campaign/pool.py`, `desktop/analyze.analyze_phase`, `build/analyze.build_tree` and `merge_resumes`, `background/analyze.phase_tree`, `is_program` and `thread_wakes` — over the repeats each pooled record lists. Check: the reconstructed wake rate of all 81 carried components with a rate matches `dataset/archetypes.yaml` within 0.2 %, and the reconstructed half-widths match the pooled records' (for example `chat-client`'s `element-desktop` ±0.5 %, `game-client`'s `steam` ±0.15 %).

Every wake was then traced as `dataset/tools/meas/session/causes.py` traces one (D27, method §5 of the 9.9 campaign: the wakeup row's waker; through a measured thread, the cause of the wake that thread was running in; after a switch-out in D, the wake before it; a process born in the phase up its creator rows to pid 1, cron or anacron, named as a job by `causes.JOBS`). What differs, because these campaigns record no cgroup census, is set out in `census_core.py`'s docstring: a waker outside the measured tree is classed by its command name against the desktop manifest (the copy at `_dev/research/jioh/task-9.10-scenarios-timelines/sources/S2-01/ubuntu-24.04.5.1-desktop-amd64.manifest`, SHA-256 `6c200933…f8ff`, checked); pid 1 and `dbus-daemon`, entries of the library, are traced on through their own rows; a measured program's own launch by run.sh is its arrival, not a harness wake; and three classes are counted apart from `outside` — `stand-in` (the programs the campaigns stand in for the desktop around the application: Xvfb for the X server, openbox for the window manager, Synapse for the Matrix server), `stimulus` (a driver process started in an operation or driven phase: the operation's trigger, the replayed input) and `harness-python` (a long-lived `python3` the trace cannot place between a harness driver and a scripted peer — the SMTP peer of the `send` operation, the local page server of `page-load`). The 9.5–9.8 workflows hold no `while kill -0 …; sleep` wait loop like `meas-session.yml`'s (grep of `meas-{interactive,playback,desktop,build,background}.yml`).

## Counts per entry

Outside-cause wakes over all repeats, by cause (`by_cause.py`). Per repeat and per component: the components table below (`per repeat, min–max`).

| section | campaign | k | wakes | outside | php-fpm | PHP session cleanup | podman | sphinxsearch | runner agent / provisioner | tracer (perf) | workflow step / run.sh | Azure VM daemons | other runner-only services |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| office-writer idle | meas-ci:interactive:2026-09-18 | 14 | 5808 | 6 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 1 | 1 |
| office-writer driven | meas-ci:interactive:2026-09-18 | 14 | 238359 | 159 | 3 | 2 | 2 | 0 | 117 | 0 | 0 | 26 | 9 |
| code-editor idle | meas-ci:interactive:2026-09-25 | 44 | 3461015 | 4360 | 10 | 90 | 59 | 0 | 3547 | 0 | 21 | 570 | 63 |
| code-editor driven | meas-ci:interactive:2026-09-25 | 43 | 17474817 | 12000 | 162 | 267 | 0 | 0 | 5256 | 0 | 38 | 6079 | 198 |
| mail-client idle | meas-ci:interactive:2026-09-19 | 77 | 91855 | 236 | 1 | 1 | 0 | 0 | 211 | 0 | 0 | 14 | 9 |
| mail-client op (send) | meas-ci:interactive:2026-09-27 | 8 | 1387082 | 541 | 0 | 0 | 0 | 0 | 486 | 0 | 0 | 21 | 34 |
| mail-client driven | meas-ci:interactive:2026-09-27 | 8 | 687204 | 879 | 21 | 0 | 0 | 0 | 721 | 0 | 0 | 117 | 20 |
| web-browser idle | meas-ci:interactive:2026-09-20 | 38 | 985296 | 1269 | 16 | 2 | 8 | 0 | 905 | 0 | 4 | 239 | 95 |
| web-browser op (page-load) | meas-ci:interactive:2026-09-20 | 38 | 2392196 | 212 | 0 | 0 | 0 | 0 | 144 | 0 | 3 | 55 | 10 |
| web-browser driven | meas-ci:interactive:2026-09-20 | 38 | 1717625 | 1509 | 5 | 2 | 0 | 0 | 1167 | 0 | 0 | 298 | 37 |
| image-editor driven | meas-ci:interactive:2026-09-18 | 5 | 26145 | 5 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 1 | 0 |
| image-editor op (unsharp-mask) | meas-ci:interactive:2026-09-18 | 5 | 7891 | 23 | 0 | 0 | 0 | 0 | 23 | 0 | 0 | 0 | 0 |
| video-editor driven | meas-ci:interactive:2026-09-18 | 20 | 2555652 | 339 | 1 | 8 | 12 | 0 | 269 | 0 | 4 | 39 | 6 |
| video-editor op (preview-render) | meas-ci:interactive:2026-09-18 | 20 | 3941719 | 36355 | 0 | 0 | 0 | 0 | 1 | 0 | 36354 | 0 | 0 |
| video-player play | meas-ci:playback:2026-09-18 | 24 | 5991548 | 1178 | 44 | 18 | 67 | 0 | 1014 | 0 | 2 | 25 | 8 |
| audio-player play | meas-ci:playback:2026-09-18 | 31 | 1935395 | 2098 | 23 | 66 | 19 | 0 | 1559 | 0 | 0 | 344 | 87 |
| video-call play | meas-ci:playback:2026-09-20 | 45 | 44331713 | 31620 | 254 | 679 | 927 | 0 | 28590 | 15 | 165 | 594 | 396 |
| chat-client idle | meas-ci:desktop:2026-09-20 | 18 | 133050 | 100 | 2 | 3 | 0 | 0 | 80 | 0 | 0 | 11 | 4 |
| game-client shown | meas-ci:desktop:2026-09-20 | 12 | 2155085 | 2274 | 6 | 89 | 0 | 0 | 1730 | 0 | 265 | 123 | 61 |
| compiler-child + build-orchestrator | meas-ci:build:2026-09-18 | 14 | 1240114 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| file-archiver | meas-ci:background:2026-09-19 | 6 | 7248470 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| game-download | meas-ci:background:2026-09-19 | 30 | 134044773 | 297868 | 1436 | 2631 | 1259 | 0 | 177002 | 67074 | 111 | 39485 | 8870 |

Over all 232,052,812 traced wakes: own 90.0 %, `stand-in` 8.0 % (almost all Xvfb), kernel 1.2 %, `harness-python` 0.40 %, desktop 0.25 % (mostly `systemd-resolved`), `outside` 0.17 %, unknown 0.02 %, `stimulus` 0.002 %. No wake traces to `sphinxsearch`. The `harness-python` wakes are 775,463 of the `send` operation's (the SMTP peer: the long-lived `python3` that wakes `Socket Thread` and, through it, the rest) and 118,909 of the `page-load` operation's (the local page server), the stand-ins for the network's other end; they are not counted as `outside` below.

## How far each value would move

Removing a wake lowers the component's count by one and its run sum by its run. The wake rate is read by its per-repeat values, the gap mean as the carried table carries it (Σ phase span / Σ wakes, the wakes wrapped round the phase) and the run mean as Σ run / Σ wakes, each against its 95 % half-width over the repeats (`meas/stability.py`; the tolerance is ±5 %) — `effect.py`. `outside (direct)`: the outside-cause wakes, and in brackets those whose own wakeup row names the outside waker; the rest inherit the cause through the chain rule (`direct.py`).

| entry | phase | component | k | wakes | outside (direct) | per repeat, min–max | wake rate: shift / half-width | gap mean | run mean |
|---|---|---|---|---|---|---|---|---|---|
| office-writer | idle | `soffice.bin` | 14 | 5808 | 6 (6) | 0–2 | -0.103 % / ±0.09 % **beyond** | +0.103 % / ±0.09 % **beyond** | -0.097 % / ±4.92 % |
| code-editor | idle | `code` | 44 | 103756 | 133 (64) | 0–16 | -0.128 % / ±0.19 % | +0.128 % / ±0.19 % | -0.016 % / ±1.25 % |
| code-editor | idle | `gpu/Chrome_ChildIOT` | 44 | 621253 | 737 (0) | 5–33 | -0.119 % / ±2.19 % | +0.119 % / ±2.19 % | -0.006 % / ±2.81 % |
| code-editor | idle | `gpu/VizCompositorTh` | 44 | 712066 | 910 (336) | 4–36 | -0.128 % / ±2.28 % | +0.128 % / ±2.28 % | +0.005 % / ±1.99 % |
| code-editor | idle | `renderer/Compositor` | 44 | 702475 | 928 (219) | 5–52 | -0.132 % / ±1.37 % | +0.132 % / ±1.37 % | +0.007 % / ±2.48 % |
| code-editor | idle | `renderer/ThreadPoolForeg` | 44 | 105700 | 103 (0) | 0–11 | -0.097 % / ±3.31 % | +0.098 % / ±3.31 % | +0.068 % / ±3.70 % |
| code-editor | idle | `renderer/code` | 44 | 601757 | 822 (272) | 4–45 | -0.137 % / ±1.72 % | +0.137 % / ±1.72 % | +0.007 % / ±2.24 % |
| code-editor | idle | `residual` | 44 | 95307 | 72 (19) | 0–10 | -0.076 % / ±0.86 % | +0.076 % / ±0.86 % | -0.003 % / ±1.60 % |
| code-editor | idle | `utility/code` | 44 | 352948 | 489 (180) | 0–70 | -0.139 % / ±3.64 % | +0.139 % / ±3.64 % | +0.024 % / ±2.29 % |
| code-editor | idle | `utility/libuv-worker` | 44 | 165753 | 166 (0) | 0–24 | -0.100 % / ±5.63 % | +0.100 % / ±5.63 % | -0.015 % / ±2.35 % |
| mail-client | idle | `IPC I/O Parent` | 77 | 1933 | 9 (0) | 0–3 | -0.466 % / ±1.73 % | +0.468 % / ±1.73 % | +0.104 % / ±1.69 % |
| mail-client | idle | `IPDL Background` | 77 | 11100 | 28 (0) | 0–7 | -0.252 % / ±0.82 % | +0.253 % / ±0.82 % | -0.049 % / ±1.04 % |
| mail-client | idle | `IndexedDB IO` | 77 | 4757 | 11 (0) | 0–3 | -0.231 % / ±1.58 % | +0.232 % / ±1.58 % | -0.068 % / ±1.69 % |
| mail-client | idle | `JS Watchdog` | 77 | 4777 | 7 (5) | 0–2 | -0.147 % / ±4.41 % | +0.147 % / ±4.41 % | +0.005 % / ±2.53 % |
| mail-client | idle | `StreamTrans` | 77 | 3695 | 10 (5) | 0–3 | -0.271 % / ±3.59 % | +0.271 % / ±3.59 % | -0.084 % / ±2.66 % |
| mail-client | idle | `Timer` | 77 | 10523 | 16 (12) | 0–3 | -0.152 % / ±1.79 % | +0.152 % / ±1.79 % | -0.040 % / ±1.83 % |
| mail-client | idle | `WebExtensions/IPC I/O Child` | 77 | 1693 | 6 (0) | 0–2 | -0.354 % / ±0.12 % **beyond** | +0.356 % / ±0.12 % **beyond** | +0.035 % / ±1.01 % |
| mail-client | idle | `WebExtensions/JS Watchdog` | 77 | 3076 | 5 (2) | 0–1 | -0.163 % / ±0.16 % **beyond** | +0.163 % / ±0.16 % **beyond** | +0.052 % / ±2.36 % |
| mail-client | idle | `WebExtensions/StreamTrans` | 77 | 2412 | 4 (1) | 0–3 | -0.166 % / ±4.67 % | +0.166 % / ±4.67 % | +0.010 % / ±4.75 % |
| mail-client | idle | `WebExtensions/Timer` | 77 | 2598 | 9 (6) | 0–3 | -0.346 % / ±2.48 % | +0.348 % / ±2.48 % | +0.088 % / ±2.71 % |
| mail-client | idle | `WebExtensions/WebExtensions` | 77 | 9567 | 27 (0) | 0–8 | -0.282 % / ±2.04 % | +0.283 % / ±2.04 % | -0.001 % / ±1.94 % |
| mail-client | idle | `glean.dispatche` | 77 | 2608 | 6 (0) | 0–3 | -0.230 % / ±1.80 % | +0.231 % / ±1.80 % | +0.013 % / ±1.44 % |
| mail-client | idle | `gmain` | 77 | 11550 | 31 (30) | 0–7 | -0.268 % / ±0.00 % **beyond** | +0.269 % / ±0.00 % **beyond** | +0.038 % / ±2.15 % |
| mail-client | idle | `residual` | 77 | 3227 | 4 (0) | 0–3 | -0.124 % / ±1.34 % | +0.124 % / ±1.34 % | -0.205 % / ±1.69 % |
| mail-client | idle | `thunderbird-bin` | 77 | 18338 | 63 (0) | 0–9 | -0.344 % / ±2.66 % | +0.345 % / ±2.66 % | +0.156 % / ±2.63 % |
| mail-client | op | `Compositor` | 8 | 350508 | 273 (0) | 0–128 | -0.078 % / ±0.77 % | +0.078 % / ±0.76 % | +0.001 % / ±4.96 % |
| mail-client | op | `Renderer` | 8 | 72209 | 68 (0) | 0–19 | -0.094 % / ±1.15 % | +0.094 % / ±1.17 % | +0.028 % / ±5.36 % |
| mail-client | op | `Socket Thread` | 8 | 434893 | 1 (0) | 0–1 | -0.000 % / ±1.06 % | +0.000 % / ±1.06 % | +0.000 % / ±3.80 % |
| mail-client | op | `Softwar~cThread` | 8 | 35462 | 24 (14) | 0–11 | -0.068 % / ±0.22 % | +0.068 % / ±0.22 % | -0.020 % / ±5.46 % |
| mail-client | op | `StreamTrans` | 8 | 32975 | 0 (0) | 0–0 | +0.000 % / ±6.51 % | +0.000 % / ±6.52 % | +0.000 % / ±18.43 % |
| mail-client | op | `SwComposite` | 8 | 44343 | 35 (0) | 0–11 | -0.079 % / ±1.59 % | +0.079 % / ±1.59 % | +0.020 % / ±5.38 % |
| mail-client | op | `TaskCon~ller` | 8 | 25261 | 9 (0) | 0–9 | -0.036 % / ±1.94 % | +0.036 % / ±1.94 % | +0.017 % / ±2.56 % |
| mail-client | op | `Timer` | 8 | 16488 | 10 (2) | 0–8 | -0.061 % / ±2.65 % | +0.061 % / ±2.66 % | -0.010 % / ±3.58 % |
| mail-client | op | `WRRende~ckend#0` | 8 | 16613 | 15 (0) | 0–4 | -0.090 % / ±2.50 % | +0.090 % / ±2.53 % | -0.000 % / ±11.16 % |
| mail-client | op | `glean.dispatche` | 8 | 16818 | 15 (0) | 0–4 | -0.089 % / ±2.47 % | +0.089 % / ±2.49 % | +0.013 % / ±8.18 % |
| mail-client | op | `residual` | 8 | 60490 | 51 (1) | 0–24 | -0.084 % / ±1.49 % | +0.084 % / ±1.49 % | -0.149 % / ±6.60 % |
| mail-client | op | `thunderbird-bin` | 8 | 281022 | 40 (0) | 0–11 | -0.014 % / ±4.05 % | +0.014 % / ±4.11 % | -0.021 % / ±4.77 % |
| web-browser | idle | `chrome` | 38 | 18248 | 25 (15) | 0–11 | -0.137 % / ±0.82 % | +0.137 % / ±0.82 % | +0.008 % / ±2.38 % |
| web-browser | idle | `gpu/Chrome_ChildIOT` | 38 | 173122 | 220 (0) | 0–13 | -0.127 % / ±0.67 % | +0.127 % / ±0.67 % | -0.003 % / ±1.98 % |
| web-browser | idle | `gpu/VizCompositorTh` | 38 | 275834 | 295 (142) | 1–16 | -0.107 % / ±1.15 % | +0.107 % / ±1.15 % | -0.021 % / ±2.11 % |
| web-browser | idle | `renderer/Compositor` | 38 | 290250 | 403 (96) | 0–21 | -0.139 % / ±0.62 % | +0.139 % / ±0.62 % | +0.004 % / ±2.78 % |
| web-browser | idle | `renderer/chrome` | 38 | 168400 | 217 (82) | 1–17 | -0.129 % / ±2.88 % | +0.129 % / ±2.88 % | -0.023 % / ±4.37 % |
| web-browser | idle | `residual` | 38 | 41126 | 84 (74) | 0–9 | -0.204 % / ±2.07 % | +0.205 % / ±2.07 % | +0.034 % / ±2.24 % |
| web-browser | idle | `utility/chrome` | 38 | 18308 | 25 (25) | 0–3 | -0.137 % / ±0.22 % | +0.137 % / ±0.22 % | +0.012 % / ±2.83 % |
| web-browser | op | `Chrome_IOThread` | 38 | 588198 | 50 (0) | 0–13 | -0.008 % / ±0.94 % | +0.009 % / ±0.95 % | +0.000 % / ±1.42 % |
| web-browser | op | `CompositorTileW` | 38 | 67163 | 27 (0) | 0–5 | -0.040 % / ±0.70 % | +0.040 % / ±0.71 % | +0.021 % / ±2.16 % |
| web-browser | op | `ThreadPoolForeg` | 38 | 148645 | 3 (0) | 0–3 | -0.002 % / ±1.84 % | +0.002 % / ±1.86 % | +0.002 % / ±2.08 % |
| web-browser | op | `chrome` | 38 | 261182 | 44 (0) | 0–11 | -0.017 % / ±0.77 % | +0.017 % / ±0.78 % | +0.005 % / ±2.28 % |
| web-browser | op | `gpu/Chrome_ChildIOT` | 38 | 149178 | 22 (0) | 0–5 | -0.014 % / ±0.60 % | +0.015 % / ±0.61 % | +0.002 % / ±1.93 % |
| web-browser | op | `gpu/VizCompositorTh` | 38 | 153204 | 32 (16) | 0–6 | -0.021 % / ±0.43 % | +0.021 % / ±0.44 % | +0.014 % / ±3.23 % |
| web-browser | op | `renderer/Chrome_ChildIOT` | 38 | 323217 | 9 (0) | 0–4 | -0.003 % / ±0.88 % | +0.003 % / ±0.88 % | +0.000 % / ±0.84 % |
| web-browser | op | `renderer/Compositor` | 38 | 138353 | 6 (1) | 0–3 | -0.004 % / ±0.98 % | +0.004 % / ±1.00 % | +0.001 % / ±1.24 % |
| web-browser | op | `renderer/ThreadPoolForeg` | 38 | 288883 | 0 (0) | 0–0 | +0.000 % / ±1.32 % | +0.000 % / ±1.33 % | +0.000 % / ±1.61 % |
| web-browser | op | `renderer/chrome` | 38 | 82714 | 8 (3) | 0–2 | -0.010 % / ±1.34 % | +0.010 % / ±1.34 % | +0.009 % / ±2.03 % |
| web-browser | op | `residual` | 38 | 109214 | 2 (2) | 0–2 | -0.002 % / ±1.44 % | +0.002 % / ±1.47 % | +0.001 % / ±1.26 % |
| web-browser | op | `utility/Chrome_ChildIOT` | 38 | 82245 | 9 (9) | 0–4 | -0.011 % / ±1.57 % | +0.011 % / ±1.59 % | +0.004 % / ±1.64 % |
| image-editor | driven | `gimp` | 5 | 26145 | 5 (5) | 0–4 | -0.019 % / ±0.55 % | +0.019 % / ±0.55 % | +0.015 % / ±4.15 % |
| image-editor | op | `gimp` | 5 | 1195 | 13 (0) | 0–13 | -1.095 % / ±4.38 % | +1.100 % / ±4.36 % | +0.675 % / ±4.36 % |
| image-editor | op | `script-fu` | 5 | 6696 | 10 (2) | 0–10 | -0.150 % / ±1.03 % | +0.150 % / ±1.03 % | -0.068 % / ±4.35 % |
| video-editor | driven | `QXcbEventQueue` | 20 | 880859 | 0 (0) | 0–0 | +0.000 % / ±1.19 % | +0.000 % / ±1.19 % | +0.000 % / ±2.56 % |
| video-editor | driven | `kdenlive` | 20 | 1652745 | 338 (335) | 10–26 | -0.020 % / ±3.47 % | +0.020 % / ±3.47 % | +0.012 % / ±5.00 % |
| video-editor | driven | `residual` | 20 | 22048 | 1 (0) | 0–1 | -0.005 % / ±1.39 % | +0.005 % / ±1.39 % | +0.003 % / ±1.33 % |
| video-editor | op | `kdenlive_render` | 20 | 3844521 | 36040 (6) | 0–21660 | -0.946 % / ±0.68 % **beyond** | +0.946 % / ±0.68 % **beyond** | -0.016 % / ±0.70 % |
| video-editor | op | `residual` | 20 | 97198 | 315 (1) | 0–189 | -0.327 % / ±0.66 % | +0.325 % / ±0.66 % | -0.179 % / ±0.64 % |
| chat-client | idle | `Chrome_ChildIOT` | 18 | 16028 | 4 (2) | 0–3 | -0.025 % / ±0.95 % | +0.025 % / ±0.95 % | +0.010 % / ±3.17 % |
| chat-client | idle | `Chrome_IOThread` | 18 | 20009 | 1 (0) | 0–1 | -0.005 % / ±0.62 % | +0.005 % / ±0.62 % | -0.013 % / ±2.19 % |
| chat-client | idle | `ThreadPoolForeg` | 18 | 45671 | 23 (9) | 0–5 | -0.050 % / ±1.79 % | +0.050 % / ±1.79 % | -0.009 % / ±2.71 % |
| chat-client | idle | `ThreadPoolServi` | 18 | 4152 | 13 (8) | 0–4 | -0.313 % / ±0.86 % | +0.314 % / ±0.86 % | +0.023 % / ±3.84 % |
| chat-client | idle | `element-desktop` | 18 | 42119 | 58 (58) | 0–9 | -0.138 % / ±0.51 % | +0.138 % / ±0.51 % | +0.036 % / ±2.92 % |
| chat-client | idle | `residual` | 18 | 5071 | 1 (1) | 0–1 | -0.020 % / ±1.87 % | +0.020 % / ±1.87 % | +0.007 % / ±4.33 % |
| game-client | shown | `CHTTPClientThre` | 12 | 57872 | 73 (73) | 2–13 | -0.126 % / ±0.31 % | +0.126 % / ±0.31 % | +0.021 % / ±3.65 % |
| game-client | shown | `CJobMgr::m_Work` | 12 | 256528 | 181 (30) | 11–24 | -0.071 % / ±0.58 % | +0.071 % / ±0.58 % | -0.012 % / ±5.67 % |
| game-client | shown | `CNet Encrypt:0` | 12 | 57889 | 56 (55) | 1–11 | -0.097 % / ±0.25 % | +0.097 % / ±0.25 % | +0.010 % / ±3.92 % |
| game-client | shown | `Chrome_ChildIOT` | 12 | 96691 | 84 (0) | 1–17 | -0.087 % / ±0.63 % | +0.087 % / ±0.63 % | -0.002 % / ±3.03 % |
| game-client | shown | `Compositor` | 12 | 133928 | 170 (23) | 2–37 | -0.127 % / ±0.88 % | +0.127 % / ±0.88 % | +0.038 % / ±4.29 % |
| game-client | shown | `IPC:CSteamEngin` | 12 | 320372 | 391 (168) | 14–60 | -0.122 % / ±0.81 % | +0.122 % / ±0.81 % | +0.029 % / ±8.78 % |
| game-client | shown | `ThreadPoolForeg` | 12 | 44447 | 24 (0) | 0–4 | -0.054 % / ±4.19 % | +0.054 % / ±4.19 % | -0.039 % / ±5.06 % |
| game-client | shown | `VizCompositorTh` | 12 | 75900 | 68 (31) | 1–11 | -0.090 % / ±1.99 % | +0.090 % / ±1.99 % | +0.007 % / ±5.63 % |
| game-client | shown | `residual` | 12 | 101899 | 102 (93) | 1–16 | -0.100 % / ±0.89 % | +0.100 % / ±0.89 % | +0.006 % / ±4.47 % |
| game-client | shown | `steam` | 12 | 500165 | 632 (481) | 28–88 | -0.126 % / ±0.15 % | +0.127 % / ±0.15 % | +0.032 % / ±10.12 % |
| game-client | shown | `steamwebhelper` | 12 | 509394 | 493 (436) | 28–56 | -0.097 % / ±0.18 % | +0.097 % / ±0.18 % | +0.002 % / ±5.27 % |

The CPU-sum values (`effect_extra.py`): an outside-cause wake can remove at most its own run from the sum, so the shift is bounded by the outside-cause wakes' run over the run the value sums (the cycle work and the per-input run over the pooled record's own totals), and a count-based mean by the outside-cause wakes over the runs it averages.

| entry | value | k | wakes | outside | outside run share | half-width | bound on the shift |
|---|---|---|---|---|---|---|---|
| `video-player` | `cycle_run` (cycle work mean) | 24 | 5991548 | 1178 | 0.011 % | ±2.86 % | −0.011 % |
| `audio-player` | `cycle_run` | 31 | 1935395 | 2098 | 0.111 % | ±4.68 % | −0.111 % |
| `video-call` | `cycle_run` | 45 | 44331713 | 31620 | 0.047 % | ±1.52 % | −0.047 % |
| `office-writer` | `input_run` (SWELL-KW) | 14 | 238359 | 159 | 0.049 % | ±4.13 % | −0.052 % |
| `code-editor` | `input_run` | 43 | 17474817 | 12000 | 0.045 % | ±4.84 % | −0.047 % |
| `mail-client` | `input_run` | 8 | 687204 | 879 | 0.190 % | ±10.41 % | −0.210 % |
| `web-browser` | `input_run` | 38 | 1717625 | 1509 | 0.081 % | ±5.90 % | −0.168 % |
| `compiler-child`, `build-orchestrator` | member steps, dispatch run | 14 | 1240114 | 0 | 0 | ±0.62–2.00 %, ±0.94 % | 0 |
| `file-archiver` | `7z_run`, `7z_block` | 6 | 7248470 | 0 | 0 | ±2.18 %, ±40.5 % | 0 |
| `game-download`, `game-download-idle` | `steamcmd_run`, `steamcmd_block` | 30 | 134044773 | 297868 (263924 direct) | 0.069 % | ±2.21 %, ±9.67 % | ≤ 0.24 % of the runs |

The playback `period` is the mean interval between cycle starts read off one reference thread (`ao`, `vo`, `utility/AudioWorkerThre`); its outside-cause wakes are among the counts above, and the period's half-width (±0.00–0.02 %) is a timer's: removing a stray wake of the reference thread does not move a cycle start that the timer sets.

## Two checks on what the outside-cause wakes are

A wakeup row names the task that was running when the wakeup was raised. A wakeup raised from interrupt context — a timer expiring, a network receive — names whichever task the interrupt found running, and on the runner the other CPUs run the harness. Two readings say most of the counts above are that, not wakes the harness or `php-fpm` caused:

- **Rows per CPU-second** (`check_irq.py`, the desktop campaign). Over Steam's 12 shown phases, the runner processes outside the tree raise 14–70 tree wakeup rows per CPU-second they ran on the other CPUs (`.NET TP Worker` 28, `.NET Tiered Com` 70, `hv_kvp_daemon` 14, each repeat's `provjobd` instance 22–48 where it is among the 25 most frequent wakers, `php8.3` 86); the programs that do talk to the tree raise thousands (Xvfb 20,921, `dbus-daemon` 4,741, `systemd-resolved` 1,482). Over Element's 18 idle phases: the runner processes 0.4–1.9 per CPU-second, Synapse 46. Unrelated processes waking the tree in proportion to their own CPU time is what interrupt-context naming gives.
- **Fixed-count components** (`fixed_count.py`). `mail-client`'s `gmain` wakes exactly 150 times in every one of the 77 idle phases; 31 of those 150-wake phases' wakes trace to the runner agent or the Azure VM daemon, 30 of them by their own wakeup row. Had those causes added the wakes, those phases would hold 151 or more. The same holds for `WebExtensions/IPC I/O Child` (22 wakes in 76 of 77 repeats; all 6 outside-cause wakes in those), `WebExtensions/JS Watchdog` (40 in 74 of 77; all 5) and `office-writer`'s `soffice.bin` (415 in 11 of 14; all 6). These are the four components whose shift exceeds their half-width (above): their half-width is a timer's, near zero, and the wakes the rule would remove are the timer's own.

The mechanism this points to — a timer of the idle measured CPU expiring on another, busy CPU (the kernel's timer migration), and network receive processing — is a reading of the data here, not verified against a primary source. Were it to be stated, the sources to read are the kernel's `kernel/time/timer_migration.c` (6.17, the runner's kernel) for where an idle CPU's timers expire, and `tools/perf/builtin-sched.c` for which task `perf sched timehist -w` prints as the waker.

The remaining exceedance, `video-editor`'s `preview-render` operation's `kdenlive_render` (−0.95 % against ±0.68 %), is of a third kind. In 4 of the 20 repeats one render's main thread was woken by `pgrep` — the operation driver's `wait_proc`, polling for the renderer process (`dataset/tools/meas/probe/ops_driver.py`, `op_kdenlive`) — 6 wakes in all, which the trace names directly (at 925.107 s in repeat 6, `pgrep[10702] awakened: kdenlive_render[10698]`). The chain rule then hands that cause to every later wake of the render's threads, which wake one another without a timer between them until the render ends: 7,165 and 7,214 wakes in two repeats (one render each, about 11 s), 21,660 in a third (three `pgrep` wakes), 1 in the fourth. The harness did raise those 6 wakes (how a `/proc` read wakes the renderer is not read here); the render's work after them is the operation's own and would run without them.

## Verdict

By D27's rule as written, every 9.5–9.8 campaign but the compile and 7-Zip ones holds outside-cause wakes — 0.1–0.5 % of a component's wakes in most, at most 1.1 % (`image-editor`'s operation `gimp`, a shift within its ±4.4 %) — and `php-fpm`, PHP's session cleanup and `podman` are among the causes in most entries, `sphinxsearch` in none. Removing them moves no carried value beyond the ±5 % tolerance, and no CPU-sum value (cycle work, per-input run, build steps, batch runs and blocks) beyond 0.25 %, against half-widths of 0.6–40 %. Five component values would move by more than their own half-width — `gmain`, `WebExtensions/IPC I/O Child` and `WebExtensions/JS Watchdog` of `mail-client`, `soffice.bin` of `office-writer` (0.10–0.35 % against ±0.00–0.16 %), and `kdenlive_render` of `video-editor`'s operation (0.95 % against ±0.68 %) — and for each the census shows the removal would be wrong: the first four's outside-cause wakes are their own fixed timer's wakes named after the task the interrupt found running, and the fifth's are one render's own work inherited from 6 driver wakes. No 9.5–9.8 component carries the kind D27 found in the session: a cause raising the same wakes at the same point of every repeat (php-fpm's 180 a phase into pid 1, the wait loop's 180 into WirePlumber). Guidebook sentence: *The 9.5–9.8 campaigns' wakes were traced to their causes as 9.9 D27 traced the session's (`_dev/research/jioh/php-fpm-census/`): 0.17 % of 232 million wakes trace to a cause outside the observed desktop, most to runner processes the trace names because an interrupt found them running, and removing them would move no carried value beyond its tolerance; the values stand as carried.*

## Not checked, and limits

- **Out of the hand-off's scope**: 9.10's campaigns on the same runner image (`video-editor`'s idle phase, `meas-ci:interactive:2026-10-05`; `renderer-hidden`, `meas-ci:desktop:2026-10-05b`; the launch phases; the 9.10 background jobs), and 9.8's `chrome-hidden` and `chrome-visible` phases, which the library no longer carries from `meas-ci:desktop:2026-09-20`. The same scripts apply.
- **No cgroup census** in these campaigns: a waker outside the tree is classed by its command name (`COMMS` in `census_core.py`); a name the table does not hold is `unknown` and kept (36,012 wakes, 0.02 %), including 31,471 `page-load` wakes whose chain is deeper than 25 hops.
- **`python3`** cannot be told apart by name between a harness driver, the pool's snapshot and a scripted peer; such wakes are `harness-python`, counted with `outside` only in the upper bound `effect.py` writes (`*_shift_up`), which moves no idle, driven or play value differently from the rule's count; in the two operations whose peer is a `python3` it is the peer.
- **The per-input run and the cycle work** are bounded, not recomputed: the bound assumes every outside-cause wake's run lies inside an input window or a cycle.
- **SteamCMD's direct split** reads each repeat's wakeup rows again from the release zips: 263,924 of the 297,868 outside-cause wakes are direct, led by `perf` (65,561: the tracer, busy on the harness CPUs while the download's network receives arrive), the runner agent's `.NET` threads and `hv_kvp_daemon` — the interrupt-context pattern of the first check, at a download's interrupt rate.

## Scripts

All run with `python3 -I` on the downloaded data, reading the committed tools (`dataset/tools/meas/`) unchanged.

| script | what it does |
|---|---|
| `census_core.py` | the tracing: `causes.py`'s rules adapted to a campaign with no cgroup census; the command-name table; the classes |
| `census_campaign.py` | 9.5's interactive and playback campaigns, per app and section |
| `census_desktop.py` | 9.8's desktop campaign (`chat-client`, `game-client`) |
| `census_build.py` | 9.6's warm `make -j8` phase, per role |
| `census_background.py` | 9.7's 7-Zip and SteamCMD phases (SteamCMD read from the zips one repeat at a time) |
| `effect.py`, `table.py` | each component value's shift against its half-width |
| `effect_extra.py` | the CPU-sum values' bounds |
| `direct.py` | the outside-cause wakes split into those the outside waker raised and those inherited through the chain |
| `by_cause.py`, `labels.py` | the counts by cause group; every non-own label per component |
| `check_irq.py`, `fixed_count.py` | the two checks |
| `render.py` | the components table |

## 9.9's own removals under the chain rule

Run 2026-10-21. 9.9 took out of its four session entries' components every wake whose cause the trace leads to outside the observed desktop (D27; `dataset/tools/meas/session/causes.py`), a wake raised by a thread running in such a wake taking that wake's cause (D27 decision 2). On a busy program that rule over-attributes: 6 `pgrep` wakes of `kdenlive_render` became 36,040, the render's threads waking one another with no timer between them (above). This section reads 9.9's own removals the same way. `<scratch2>` is `/private/tmp/claude-501/-Users-jiohin-Desktop-future-of-sw-LLM-driven-shceduling/43e369a1-b5c7-40a2-b57d-cc4fcdb568dc/scratchpad/phpfpm2`. The releases of this section and the next were downloaded again into `<scratch2>/rel/`, each of the 241 assets' sha256 equal to `dataset/meas-releases.yaml`'s; the outputs are in `<scratch2>/out/`.

### What ran

Release `meas-ci-session-2026-09-24`, the 24 pooled repeats. `session/pool.py`, unchanged, reproduces the committed `_dev/research/jioh/task-9.9-daemons-session/campaign/results/pooled.json` exactly: all 18 carried values with their half-widths and carried status, and every entry's causes, components and tables. `session/fold_in.py` on it gives `compositor-shell`, `audio-server`, `service-manager` and `message-bus` as `dataset/archetypes.yaml` carries them. `session_split.py` runs the same pool with `causes.Causes` replaced, inside `session/analyze.py` at run time, by a subclass that records for each wake that leaves how its cause reached it and the row the cause was read from; its class and label equal `Causes.cause`'s for all 48,245 entry wakes. The four ways a cause reaches a wake:

- **direct**: the wake's own wakeup row names the outside waker;
- **chain**: an entry thread woke it while running in a wake whose cause is outside;
- **D-continuation**: it continues the wake before it after a switch-out in D (pid 1 waiting for an RCU grace period);
- **follow-up**: WirePlumber's worker's own timer, firing 100.2 ms after a wake, takes that wake's cause (`FOLLOW_UP`).

### Counts

Over the 24 repeats, per repeat min–max in brackets; wakes kept are the carried component's.

| entry | component | wakes kept | outside | direct | chain | D-continuation | follow-up | by cause |
|---|---|---|---|---|---|---|---|---|
| `message-bus` | `system-bus/dbus-daemon` | 603 | 5,236 | 0 | 5,236 (192–264) | 0 | 0 | `php8.3-fpm` 4,989, PHP's session cleanup 149, `podman` 92, `systemd-networkd` 6: all chain |
| `service-manager` | `pid1/systemd` | 3,034 | 4,671 | 4,550 (186–193) | 0 | 121 (0–11) | 0 | `php8.3-fpm` 4,316 direct and 109 D-continuation; `systemd-networkd` 201 and 3; `podman` 9 and 9; PHP's session cleanup 24 direct |
| `audio-server` | `wireplumber/gmain` | 402 | 8,759 | 4,429 (183–187) | 1 | 0 | 4,329 (175–181) | the harness 4,351 direct (4,317 of them the workflow's wait loop, `bash`) and 4,306 follow-up; PHP's session cleanup 70 direct, 23 follow-up, 1 chain; `podman` 8 direct |
| `compositor-shell` | `gnome-shell/gmain` | 10,793 | 3 | 0 | 3 (0–1) | 0 | 0 | `php8.3-fpm` 3 |
| `compositor-shell` | `gnome-shell/gnome-shell` | 1,501 | 1 | 0 | 1 | 0 | 0 | `php8.3-fpm` 1 |
| `compositor-shell` | `gnome-shell/JS Helper` | 13,068 | 0 | — | — | — | — | — |

In all, 18,678 outside-cause wakes: 8,987 direct, 5,241 chain, 4,329 follow-up, 121 D-continuation. The user manager's 8 (`podman`, direct) belong to no carried component. The wakes that leave as events, desktop jobs bound to a clock time (D23's form), split the same way and stay out in every reading below: `message-bus` 70, all chain; `audio-server` 51, 37 direct and 14 follow-up; pid 1 37, 35 direct and 2 D-continuation. `direct.py`'s reading (the last row at or before the wake names an outside waker) agrees for the worker (4,429) and the bus (0); for pid 1 it gives 4,565, the own rows of 15 D-continuation wakes naming an outside waker and most of the rest an `rcu_` kernel thread.

### The inherited runs

Each of the 8,987 outside rows a cause was read from reaches 1–22 wakes: 2 for 8,380 of them, 1 for 310, 3 for 192. The largest, one `podman` row in repeat 47, reaches 22 wakes (pid 1's 4, the bus's 18) within 12.7 ms, through 2 threads and at most 4 hops; the largest `php8.3-fpm` rows reach 11–15 within 9–20 ms. From the row to an inherited wake: median 8.9 ms, at most 101.2 ms; every chain and D-continuation wake within 25 ms, every follow-up at 100.2 ms (median) to 100.3 ms (99th percentile). The commonest form, 4,052 rows, is an outside process signalling pid 1 and pid 1, in that run, waking the bus once: 4,743 of the bus's 5,236 wakes are one hop from their row, the rest 2–4 hops of pid 1 and the bus answering each other within the same burst (median 0.3 ms, at most 24.9 ms after the row). pid 1's D-continuation wakes come 10 ms (median) to 24 ms after the row and run 0.51 ms on average, against the component's 0.171 ms: the rest of the run the outside row started, resumed after an RCU wait. None has the `kdenlive_render` form.

### How far each value would move with the inherited wakes put back

Re-pooled by `session/pool.py`'s own reading: (ii) only the direct wakes removed, the chain, D-continuation and follow-up wakes put back; (iii) the direct and follow-up wakes removed, the chain and D-continuation wakes put back. The rule as written reproduces the committed values exactly. "D29" marks a value carried with its half-width over the 24 repeats, its spread lying in part between sessions (9.9 D29, D48).

| component | value | carried | half-width | (ii) | (iii) |
|---|---|---|---|---|---|
| `gnome-shell/JS Helper` | wake rate · gap mean · run mean | 0.3025 /s · 3305.8 ms · 0.0137 ms | ±0.73 · ±0.73 · ±1.01 % | 0 · 0 · 0 | 0 · 0 · 0 |
| `gnome-shell/gmain` | wake rate · gap mean · run mean | 0.2498 /s · 4002.6 ms · 0.0497 ms | ±0.05 · ±0.05 · ±2.15 % | +0.03 · −0.03 · −0.00 % | the same |
| `gnome-shell/gnome-shell` | wake rate · gap mean · run mean | 0.0347 /s · 28780.9 ms · 5.6996 ms | ±1.49 · ±1.49 · ±2.82 % | +0.07 · −0.07 · −0.04 % | the same |
| `wireplumber/gmain` | wake rate | 0.0093 /s | ±4.48 % | +1077 % (0.110 /s) **beyond both** | +0.25 % |
| | gap mean | 107,463 ms | ±4.48 % | −91.5 % **beyond both** | −0.25 % |
| | run mean | 0.035 ms | ±2.82 % | +2.18 % | −0.03 % |
| `pid1/systemd` | wake rate | 0.0702 /s | ±1.87 % | +3.99 % **beyond the half-width** | the same |
| | gap mean | 14,238.6 ms | ±1.87 % | −3.84 % **beyond the half-width** | the same |
| | run mean | 0.171 ms (D29) | ±7.77 % | +7.61 % (0.184 ms) **beyond ±5 %** | the same |
| `system-bus/dbus-daemon` | wake rate | 0.0140 /s (D29) | ±11.05 % | +868 % (0.135 /s) **beyond both** | the same |
| | gap mean | 71,641.9 ms (D29) | ±11.05 % | −89.7 % **beyond both** | the same |
| | run mean | 0.121 ms (D29) | ±10.74 % | +129.8 % (0.278 ms) **beyond both** | the same |

Under (ii) the rule would fail on `wireplumber/gmain`'s run mean (±5.33 %), which D29 does not carry; under (iii) it holds, the bus's three values passing outright (±2.58, ±2.58, ±2.79 %) with `php8.3-fpm`'s relay every 10 s in them. Each move is the inherited wakes' own form. The bus put back is the bus before D27 (0.135 wakes/s against the 0.137 D27 recorded), every one of its outside-cause wakes pid 1's relay inside a run an outside row began, the 99.95 % D27 read. The worker's move under (ii) is its 4,329 follow-ups, each 100.2–100.3 ms after a wake the wait loop raised (D27: 4,316 of the loop's 4,320 wakes followed so). pid 1's is its 121 D-continuation wakes.

### Verdict

Of the 18,678 wakes D27's rule took out of the session entries, 8,987 were raised by the outside cause's own row. The rest reached their component within 25 ms of that row, through pid 1 relaying it to the bus or a resumed RCU wait, or 100.2 ms after it through WirePlumber's timer it armed. No outside row reaches more than 22 wakes, and none hands its cause to a program's own work as the render's `pgrep` wakes did. The inherited wakes are the indirect wakes D27's decision 2 takes out, and the values stand as carried. Guidebook sentence: *9.9's removals were traced as the census traced 9.5–9.8's (`_dev/research/jioh/php-fpm-census/`): of the 18,678 wakes taken out of the session entries, 8,987 were raised by the outside cause itself, and the rest followed it within 25 ms through pid 1's relay to the system bus or a resumed kernel wait, or 100.2 ms later through WirePlumber's timer; no inherited run resembles the Kdenlive render's, and the values stand as carried.*

### Not checked

- What pid 1 sends the bus on each `php8.3-fpm` notification is not read from a primary source; only the trace's order and timing are stated.
- Root rows whose waker the trace prints as `9` (24 of PHP's session cleanup, 8 of `podman`) or with no comm (`:<pid>`) are placed by `Causes` through ancestry and not looked at further.
- The within-run spreads of pid 1's run mean and the bus's values (9.9's placement of each spread within one run against across the repeats, D28, D35, D48) are not re-read under (ii) or (iii).

### Scripts

| script | what it does |
|---|---|
| `session_split.py` | the subclass of `causes.Causes` recording how each leaving wake's cause reached it and its root row; the session pool as written, (ii) and (iii) |

## The 9.10 campaigns on the same runner image

Run 2026-10-21, on every carried value of a campaign in 9.10's span that counts wakes or sums their runs, by the census's method: each repeat read as its pool reads it, every wake traced by `chain_roots.py` (census_core's rules and classes, checked wake by wake against `census_core.Tracer`: 0 differences in every section), how its cause reached it and the row it was read from kept, `harness-python` and `stimulus` counted apart from `outside`. `census_core`'s command-name table is unchanged.

### What ran

| campaign (tag) | release | entries and carried phase | repeats traced |
|---|---|---|---|
| `meas-ci:interactive:2026-10-05` | `meas-ci-interactive-2026-10-05` | `video-editor` idle components (`kdenlive`, `Qt bearer threa`), the 180 s phase after the 240 s settle | 16 |
| `meas-ci:desktop:2026-10-05b` | `meas-ci-desktop-2026-10-05b` | `renderer-hidden` steady components, 12 measured renderers a repeat; its launch phase, a stream per renderer | 5, 5 |
| `meas-ci:desktop:2026-10-05` | `meas-ci-desktop-2026-10-05` | `video-editor` launch phase (the re-trace to the 240 s settle) | 5 |
| `meas-ci:desktop:2026-10-04b` | `meas-ci-desktop-2026-10-04b` | launch phases of `office-writer`, `mail-client`, `web-browser`, `video-player`, `audio-player`, `video-call` (the call opened in a running Chrome), `chat-client`, `game-client` | 5 each |
| `meas-ci:background:2026-10-01` | `meas-ci-background-2026-10-01` | `package-upgrade` (the unattended upgrade, `upgrade-install`) | 9 |
| `meas-ci:background:2026-10-02` | `meas-ci-background-2026-10-02` | `module-build-orchestrator`, `module-compiler-child` (`dkms-install`, the hook run that built the module) | 26 landings |
| `meas-ci:background:2026-10-02b` | `meas-ci-background-2026-10-02b` | `file-indexer` (the Tracker index, `tracker-index`, within the job's window) | 18 |
| `meas-ci:background:2026-10-03` | `meas-ci-background-2026-10-03` | `cpu-batch`'s `python3` (the MNIST training run, `mnist-train`) | 6 |
| `meas-ci:background:2026-10-03b` | `meas-ci-background-2026-10-03b` | `video-transcoder` (the HandBrakeCLI transcode, `handbrake-transcode`) | 5 |
| `meas-ci:background:2026-10-03c` | `meas-ci-background-2026-10-03c` | `cpu-batch`'s `kdenlive_render` (the Kdenlive export, `kdenlive-export`) | 30 |
| `meas-ci:background:2026-10-04` | `meas-ci-background-2026-10-04` | `incremental-backup` (the Déjà Dup backup, `dejadup-incremental`, to deja-dup's exit) | 28 |

The background CPU totals are also the timelines' `total_work`. Not traced: the Chrome tab-set campaign (`meas-ci:desktop:2026-10-04`), which the timelines carry as a count of `renderer-hidden` tasks, not a wake value; 10-04b's `kdenlive` and `chrome-hidden` launches, which the re-traces replace; the MNIST campaign's `madvise` check and every dry or probe job.

Check: `video-editor`'s six idle values reproduce exactly (`kdenlive` 1.1611 wakes/s ±1.71 %, gap mean 861.25 ms, run mean 0.0261 ms ±4.45 %; `Qt bearer threa` 0.1 wakes/s ±0.00 %, run mean 0.4237 ms ±1.77 %). `renderer-hidden`'s per-renderer rates equal the library's, and its rate and gap half-widths the pooled record's; its run-mean half-widths are within 0.13 points, `campaign/pool.py`'s `table_pairs` rebuilding the sums from per-repeat means rounded to four places. Each of the 50 launch landings equals the committed `dataset/launch/launch-<entry>.json.gz` wake by wake. The 78 background quantities (each batch job's run between voluntary blocks, block per run and CPU total; the module build's 56 member steps, make's dispatch, the tail's run and block and the carried CPU total) reproduce within 2.2 × 10⁻⁵.

Classes as the census has them, and: the loopback page server named by `httpd.pid` is `harness-python` (6 wakes, `renderer-hidden`'s launch); the `chrome` the harness runs to open the call page in the running browser is `stimulus` (`video-call`'s launch, 4 a repeat); Synapse by `synapse.pid` is `stand-in`.

### Counts per entry

The rule as census_core applies it (`by_cause.py`'s groups).

| section | campaign | k | wakes | outside | php-fpm | PHP session cleanup | podman | sphinxsearch | runner agent / provisioner | tracer (perf) | workflow step / run.sh | Azure VM daemons | other runner-only services |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| video-editor idle | meas-ci:interactive:2026-10-05 | 16 | 3640 | 18 | 0 | 0 | 8 | 0 | 5 | 0 | 0 | 5 | 0 |
| renderer-hidden steady | meas-ci:desktop:2026-10-05b | 5 | 7588 | 4 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| launch office-writer | meas-ci:desktop:2026-10-04b | 5 | 4254 | 128 | 0 | 0 | 0 | 0 | 43 | 0 | 84 | 1 | 0 |
| launch mail-client | meas-ci:desktop:2026-10-04b | 5 | 65614 | 217 | 0 | 0 | 0 | 0 | 20 | 0 | 190 | 0 | 7 |
| launch web-browser | meas-ci:desktop:2026-10-04b | 5 | 125835 | 270 | 5 | 0 | 2 | 0 | 55 | 6 | 187 | 14 | 1 |
| launch video-player | meas-ci:desktop:2026-10-04b | 5 | 126982 | 278 | 0 | 0 | 0 | 0 | 20 | 0 | 255 | 3 | 0 |
| launch audio-player | meas-ci:desktop:2026-10-04b | 5 | 34598 | 259 | 0 | 0 | 0 | 0 | 20 | 0 | 239 | 0 | 0 |
| launch video-call | meas-ci:desktop:2026-10-04b | 5 | 2080805 | 518 | 0 | 0 | 0 | 0 | 512 | 0 | 0 | 2 | 4 |
| launch chat-client | meas-ci:desktop:2026-10-04b | 5 | 48795 | 2598 | 0 | 0 | 0 | 0 | 0 | 0 | 2598 | 0 | 0 |
| launch game-client | meas-ci:desktop:2026-10-04b | 5 | 1554842 | 2652 | 12 | 72 | 0 | 0 | 1244 | 0 | 853 | 433 | 38 |
| launch video-editor | meas-ci:desktop:2026-10-05 | 5 | 10826 | 14 | 0 | 0 | 3 | 0 | 7 | 0 | 4 | 0 | 0 |
| launch renderer-hidden | meas-ci:desktop:2026-10-05b | 5 | 42103 | 21 | 0 | 3 | 0 | 0 | 12 | 0 | 0 | 5 | 1 |
| package-upgrade | meas-ci:background:2026-10-01 | 9 | 132088 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| module build | meas-ci:background:2026-10-02 | 26 | 931467 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| file-indexer | meas-ci:background:2026-10-02b | 18 | 378343 | 43105 | 0 | 0 | 4 | 0 | 0 | 0 | 43101 | 0 | 0 |
| cpu-batch (`python3`) | meas-ci:background:2026-10-03 | 6 | 120 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| video-transcoder | meas-ci:background:2026-10-03b | 5 | 3711965 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| cpu-batch (`kdenlive_render`) | meas-ci:background:2026-10-03c | 30 | 256908 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| incremental-backup | meas-ci:background:2026-10-04 | 28 | 2359824 | 70929 | 0 | 0 | 0 | 0 | 14 | 0 | 70914 | 1 | 0 |

The video-transcoder's 10 are `multipathd`'s. Over the 4,105,882 desktop and interactive wakes: own 91.20 %, `stand-in` 8.25 % (Xvfb; Synapse's 24,270 in `chat-client`'s launch), desktop 0.28 % (mostly a `dbus-daemon` acting on its own and `systemd-resolved`), `outside` 0.170 %, unknown 0.090 %, kernel 0.005 %, `harness-python` 57 wakes, `stimulus` 20. The unknown are 2,438 wakes by `gdbus`, the D-Bus worker threads of udisksd, polkitd, packagekitd and the desktop portals, all desktop packages but classed by the thread's name, and 1,166 chains deeper than 25 hops in `renderer-hidden`'s launch. The background jobs: `package-upgrade` own 99.33 %, kernel 0.67 %; the module build all own; `file-indexer` own 88.51 %, `outside` 11.39 %, desktop 0.10 %; the training run's 120 wakes own, the run preempted rather than woken; `video-transcoder` own but for the 10 and 3 kernel; `kdenlive_render` `stand-in` 99.62 % (Xvfb), own 0.22 %, unknown 0.16 %; `incremental-backup` desktop 92.40 %, own 4.37 %, `outside` 3.01 %, `stand-in` 0.22 %. `harness-python` and `stimulus` are 0 in every background job.

Two of these counts are the tracing's own form, not the phase's causes:

- **The launch phases' start.** Each launch phase begins at the application's exec. `launch_app` in `dataset/tools/meas/desktop/run.sh` forks the process, which runs about 0.4 ms and blocks in D before its exec; the row that ends the block names whatever ran then: the subshell recording the affinity, `$(taskset -p "$APP_PID" | sed …)`, in 21 of the 45 launches it starts, the idle task in 22, a `.NET` runner thread and `sed` in one each (audio-player repeat 1: `bash[2637]` forks 4736, which runs 0.430 ms and blocks; `bash[4737]` wakes it; the exec of `/usr/bin/mpv` follows 4 ms later). The phase cuts off the fork wake and the block, so neither the launch rule nor the D rule reaches them, and the run that execs the application (40–56 ms for mpv and Kdenlive) traces to that row; the chain rule hands it to the whole start-up, the wrapper scripts, Element's V8 workers, Steam's setup scripts. Traced on the tree's wakes from the trace's start, 2 s before the exec (census_core's rules, with the predecessors the phase's start cuts off), the launch phases' outside-cause wakes fall from 6,955 to 2,503 (0.061 %): runner processes the trace names as interrupt context, 6–62 tree rows a CPU-second against Xvfb's 4,800–17,800 and `systemd-resolved`'s 628–2,804.
- **The jobs' own session.** The Tracker index and the Déjà Dup backup run in a session bus of the user's own, which the harness opens with `dbus-run-session` in the chroot (each campaign's `method.md`). census_core names a process born in the phase after its long-lived ancestor, and the session's services descend from the runner's step shell, so every wake they raise is `the harness (workflow step / run.sh)`: in the Tracker index `gvfsd-fuse` 22,438, `gvfsd` 17,245, gvfs's volume monitors 1,343, GNOME Online Accounts 82; in the Déjà Dup backup `gvfsd` 68,002, `xdg-desktop-portal` 1,628, `gvfsd-metadata` 388, `dconf-service` 156 and the session bus's helpers. Each is a desktop package in the manifest (matched by executable name). With those executables classed by their package (`census_bg910.py --session-by-package`), the Tracker index holds 1,640 outside-cause wakes (0.43 %) and the Déjà Dup backup 15.

### How far each value would move

The idle and steady components (`effect_split.py`): the rule as written, and with only the wakes whose own row names the outside waker removed (the inherited put back).

| entry | phase | component | k | wakes | outside (direct) | per repeat, min–max | wake rate: shift / half-width | gap mean | run mean | direct only |
|---|---|---|---|---|---|---|---|---|---|---|
| video-editor | idle | `kdenlive` | 16 | 3344 | 18 (18) | 0–6 | −0.538 % / ±1.71 % | +0.541 % / ±1.71 % | −1.282 % / ±4.45 % | the same |
| video-editor | idle | `Qt bearer threa` | 16 | 288 | 0 (0) | 0–0 | 0 / ±0.00 % | 0 / ±0.00 % | 0 / ±1.77 % | — |
| renderer-hidden | steady | `HangWatcher` | 5 | 3600 | 3 (3) | 0–2 | −0.083 % / ±0.00 % **beyond** | +0.083 % / ±0.00 % **beyond** | +0.015 % / ±17.95 % | the same |
| renderer-hidden | steady | `chrome` | 5 | 2409 | 1 (1) | 0–1 | −0.042 % / ±1.59 % | +0.042 % / ±1.59 % | −0.013 % / ±11.43 % | the same |
| renderer-hidden | steady | `Chrome_ChildIOT`, `Compositor`, `PerfettoTrace`, residual | 5 | 634, 300, 300, 345 | 0 | 0 | 0 | 0 | 0 | — |

`HangWatcher` wakes 720 times in each of the 5 repeats (12 renderers × 60), and all 3 outside-cause wakes fall in those repeats: its own 10 s timer's wakes, named after the runner task the interrupt found running (the runner processes raise 3.3–5.9 tree rows a CPU-second, Xvfb 18,308), the census's fixed-count case. `video-editor`'s `kdenlive` holds 8 direct wakes by the `podman` job in repeats 8 and 12, 4 in each, at 107 tree rows a CPU-second against the runner processes' 0.5–8.8; the mechanism is not read here.

The launch phases carry each repeat's stream as observed, with no half-width (9.10 D136); "spread" is the 95 % half-width of the 5 per-repeat values, a reading of the repeats. In brackets the worst repeat.

| entry | k | wakes | outside (direct) | per repeat, min–max | CPU: shift / spread | wakes: shift / spread | CPU, direct only | read from 2 s before the exec: outside, CPU shift |
|---|---|---|---|---|---|---|---|---|
| office-writer | 5 | 4254 | 128 (2) | 0–43 | −1.54 % (−2.74 %) / ±1.96 % | −3.01 % (−5.13 %) / ±1.40 % | −0.01 % | 1, −0.00 % (−0.02 %) |
| mail-client | 5 | 65614 | 217 (7) | 0–198 | −0.51 % (−2.46 %) / ±3.07 % | −0.33 % (−1.51 %) / ±0.39 % | −0.00 % | 27, −0.01 % (−0.03 %) |
| web-browser | 5 | 125835 | 270 (34) | 21–68 | −2.64 % (−3.74 %) / ±9.26 % | −0.21 % (−0.27 %) / ±2.40 % | −0.02 % | 83, −0.04 % (−0.05 %) |
| video-player | 5 | 126982 | 278 (9) | 0–138 | −0.76 % (−2.17 %) / ±10.05 % | −0.22 % (−0.57 %) / ±6.16 % | −0.52 % (−1.49 %) | 23, −0.00 % (−0.01 %) |
| audio-player | 5 | 34598 | 259 (8) | 4–122 | **−6.76 % (−18.23 %)** / ±4.61 % | −0.75 % (−1.78 %) / ±1.13 % | −4.52 % (−12.52 %) | 20, −0.04 % (−0.07 %) |
| video-call | 5 | 2080805 | 518 (96) | 74–189 | −0.01 % (−0.01 %) / ±1.30 % | −0.02 % (−0.05 %) / ±0.45 % | −0.00 % | 518, −0.01 % (−0.01 %) |
| chat-client | 5 | 48795 | 2598 (2) | 0–1303 | **−9.55 % (−23.45 %)** / ±4.21 % | **−5.32 % (−13.36 %)** / ±0.13 % | −0.22 % (−0.58 %) | 0, 0 |
| game-client | 5 | 1554842 | 2652 (962) | 214–795 | −0.37 % (−0.87 %) / ±8.80 % | −0.17 % (−0.26 %) / ±0.99 % | −0.04 % | 1800, −0.07 % (−0.10 %) |
| video-editor | 5 | 10826 | 14 (14) | 1–4 | −1.50 % (−2.19 %) / ±3.77 % | −0.13 % (−0.18 %) / ±1.20 % | −1.50 % (−2.19 %) | 10, −0.01 % (−0.02 %) |
| renderer-hidden (12 streams) | 5 | 42103 | 21 (13) | 0–8 | −0.03 % (−0.04 %) / ±3.69 % | −0.05 % (−0.10 %) / ±7.23 % | −0.02 % | 21, −0.03 % (−0.04 %) |

Under the rule as written `audio-player`'s CPU and `chat-client`'s CPU and wakes move beyond ±5 % and their spread, `office-writer`'s wakes beyond their spread, and the first 10 s slice loses up to 25.8 % of its CPU (`audio-player`). The direct reading does not remove the move where the direct wake is the start-up run itself (`audio-player`'s 56 ms). Read from 2 s before the exec, no repeat's stream moves by more than 0.22 % of its wakes (`game-client`) or 0.10 % of its CPU.

The background values, by `effect_extra.py`'s bound (the outside-cause wakes' run over the run a value sums; their count over the runs a count-based mean averages; the larger) and recomputed (`census_bg910.py`: each repeat's values read again with the outside-cause wakes' segments taken out, their time left to the program's other threads or idle), under the rule as written and with the inherited put back. Half-widths are the pooled records'.

| entry | value | k | wakes | outside (direct) | outside run share | half-width | bound | bound, inherited put back | recomputed | recomputed, inherited put back |
|---|---|---|---|---|---|---|---|---|---|---|
| package-upgrade | run between blocks · block per run · CPU total | 9 | 132088 | 0 | 0 | ±3.10 · ±5.97 · ±3.78 % | 0 | 0 | 0 | 0 |
| module build | 56 member steps; make's dispatch · tail run · tail block · carried CPU total | 26 | 931467 | 0 | 0 | ±0.67–4.13 %; ±0.72 · ±1.82 · ±8.35 · ±1.46 % | 0 | 0 | 0 | 0 |
| file-indexer | run between blocks | 18 | 378343 | 43105 (1167) | 15.615 % | ±1.12 % | 15.6 % **beyond** | 0.31 % | −4.77 % **beyond** | +0.29 % |
| file-indexer | block per run | 18 | | | | ±3.58 % | 11.4 % **beyond** | 0.31 % | +156.5 % **beyond** | +0.47 % |
| file-indexer | CPU total | 18 | | | | ±0.28 % | 15.6 % **beyond** | 0.019 % | −15.62 % **beyond** | −0.019 % |
| file-indexer, session by package | run · block · CPU total | 18 | 378343 | 1640 (33) | 0.030 % | ±1.12 · ±3.58 · ±0.28 % | 0.43 · 0.43 · 0.030 % | 0.009 · 0.009 · 0.001 % | +0.41 · −0.07 · −0.030 % | +0.008 · +0.004 · −0.001 % |
| cpu-batch (`python3`) | run · block · CPU total | 6 | 120 | 0 | 0 | ±27.3 · ±10.8 · ±4.04 % | 0 | 0 | 0 | 0 |
| video-transcoder | run · block · CPU total | 5 | 3711965 | 10 (6) | 0.000 % | ±1.79 · ±36.1 · ±2.64 % | 0.000 % | 0.000 % | 0.000 % | 0.000 % |
| cpu-batch (`kdenlive_render`) | run · block · CPU total | 30 | 256908 | 0 | 0 | ±0.77 · ±13.1 · ±0.80 % | 0 | 0 | 0 | 0 |
| incremental-backup | run between blocks | 28 | 2359824 | 70929 (213) | 3.506 % | ±4.38 % | 3.51 % | 0.009 % | −0.52 % | +0.009 % |
| incremental-backup | block per run | 28 | | | | ±6.19 % | 3.01 % | 0.009 % | +1,906.6 % **beyond** | +0.30 % |
| incremental-backup | CPU total | 28 | | | | ±0.56 % | 3.51 % **beyond** | 0.000 % | −3.51 % **beyond** | −0.000 % |
| incremental-backup, session by package | run · block · CPU total | 28 | 2359824 | 15 (15) | 0.000 % | ±4.38 · ±6.19 · ±0.56 % | ≤ 0.001 % | ≤ 0.001 % | +0.001 · +0.001 · −0.000 % | the same |

The inherited wakes carry almost all the outside-cause run: in the Tracker index 110,705 ms against the direct wakes' 136 ms, in the Déjà Dup backup 162,613 ms against 16 ms. The bound for a block mean counts the runs removed only, and recomputing shows how far it understates when the removed runs' time is large against the blocks': 11.4 % against +156.5 %, 3.0 % against +1,906.6 %. A removed run's time becomes the program's idle time, which widens the block it falls in.

### The inherited runs

Here the chain rule does hand single rows to programs' own work, in the form of the `kdenlive_render` case:

- the Tracker index, in each of the 18 repeats: one `gvfsd-fuse` row reaches 1,195–1,336 wakes over 5.93–5.99 s, through 15 threads and 964–1,224 hops — the extractor's `single` thread, the miner, its pool and `tracker-extract`;
- the Déjà Dup backup: one `gvfsd` D-Bus worker row reaches 51,389 wakes over 100.4 s through 29 threads in repeat 8, the whole backup (`gpg` 19,839, `deja-dup` 18,732, `duplicity` 12,742), and 16,448 over 60.0 s in repeat 29;
- in kept classes, with no effect on a value: one Xvfb row (`stand-in`) reaches 8,266 wakes over 16.2 s, the whole export, in the Kdenlive export's repeat 1; one `systemd-resolved` row (desktop) 52,358 over 106 s in the Déjà Dup backup's repeat 1;
- the launch phases: one `bash` row reaches 1,295 and 1,303 wakes (`chat-client` repeats 2 and 4, 0.75–0.79 s, 16 threads, 1,250 of them `V8Worker`), 521 and 331 (`game-client` repeats 1 and 3, Steam's `setup.sh`), 190 (`mail-client` repeat 5); these are the cut-off start of the first item above. One `hv_kvp_daemon` row reaches 349 wakes in 9 ms through Steam's threads in `game-client`'s repeat 5, an interrupt-context naming handed on, 0.11 % of that repeat's wakes, and stays when the launch is read from before its exec.

The idle and steady components hold no inherited outside-cause wake.

### Verdict

Under census_core's rule as written, 1.02 % of the 11,876,597 traced wakes trace outside the observed desktop, and values move beyond their half-width in three places: `renderer-hidden`'s `HangWatcher` (0.083 % against ±0.00 %), three launch streams (`audio-player`'s CPU −6.76 %, `chat-client`'s CPU −9.55 % and wakes −5.32 % over the repeats, `office-writer`'s wakes −3.01 % against their spread), and the Tracker index's and the Déjà Dup backup's batch values (the index's CPU total −15.6 %, its block per run +157 % and its run between blocks −4.8 %; the backup's block per run +1,907 % and CPU total −3.5 %). In each the trace shows the removal would be wrong: `HangWatcher`'s are its own fixed timer's wakes; the launch streams' are the launched process's own start-up, traced to the harness because the phase's start cuts off the fork that began it; the batch values' are the jobs' own work, handed by the chain rule from the desktop services of the session the harness opens for the user. Read with the launches from before their exec and the session's services by their package, 0.035 % of the wakes trace outside (4,190), no launch stream moves by more than 0.22 % of a repeat's wakes or 0.10 % of its CPU, no batch value by more than 0.41 %, and no component value beyond its half-width but `HangWatcher`'s (the largest other the idle `kdenlive`'s run mean, −1.28 % against ±4.45 %); with only the wakes whose own row names the outside cause removed, no batch value moves beyond 0.47 %. The values stand as carried.

**Decision (인지오, 2026-10-21): the session's services are classed by their package.** The desktop services of the session the harness opens for the Tracker index and the Déjà Dup backup (gvfs, the portals, dconf, GNOME Online Accounts) are classed by their package, as D27's rule defines outside — a package Ubuntu 24.04's desktop manifest does not hold, or the harness; all four are in the manifest. census_core's ancestry rule, which names them the harness, is the census's approximation for campaigns with no cgroup census, and it yields to D27's definition here, as the stand-ins (Xvfb, openbox, Synapse) are counted apart from `outside`. Read so, no batch value moves by more than 0.41 %.

**Decision (인지오, 2026-10-21): the launch phases are read from 2 s before the exec.** The trace holds the launched tree from 2 s before the exec, and read from there census_core's launch rule (a measured program's launch by `run.sh` is its arrival) sees the fork the phase's start cuts off. The rule-as-written figures above are the phase window's artefact and stay as such. Read so, no launch stream moves by more than 0.22 % of a repeat's wakes or 0.10 % of its CPU.

**Decision (인지오, 2026-10-21): the chain rule keeps no stopping point.** The rule is left as it is; its limit — checked only on the idle session entries, unbounded inheritance on a busy program, and the direct/inherited split to read before any use beyond them — is written into `dataset/tools/meas/session/causes.py`'s docstring.

Guidebook sentence: *The 9.10 campaigns' wakes were traced to their causes as 9.9 D27 traced the session's (`_dev/research/jioh/php-fpm-census/`): the upgrade, the module build, the training run, the transcode and the Kdenlive export hold no outside-cause wake but 10 of `multipathd`'s; the rest the rule would take out are runner processes named by interrupt context, the launched applications' own start-up cut off at the exec, and the Tracker index's and the Déjà Dup backup's own work reached through the desktop services of the session the harness opens for them; read so, no carried value moves beyond its half-width but `HangWatcher`'s timer, by 0.08 %, and the values stand as carried.*

### Not checked

- The launch reading from before the exec and the session-by-package reading are this section's, not D27's rule as census_core implements it; both are the record's basis by 인지오's decisions of 2026-10-21 (Verdict). Why the launched process blocks in D right after its fork, and why the subshell's row ends the block, is not read against the kernel's source.
- The session services are matched to their packages by executable name, not by the packages' file lists.
- 412 wakes by `kdenlive` and its `QDBusConnection` thread, the application that starts the export, are unknown and kept; Kdenlive is not in the desktop manifest. Taken out, their run share (0.94 %) would exceed the export's CPU total's ±0.80 %; their count share is 0.16 %.
- census_core keeps each wake's cause once traced, and a chain cut at its 25-hop limit is kept as `unknown: chain too deep` along its whole length: read in the census's order the module build is 95.84 % such unknowns, traced in time order (`census_bg910.py --warm`) every wake its own. The census's 31,471 `page-load` wakes deeper than 25 hops (above) are not re-read this way.
- The recomputation leaves a removed run's time idle or to the program's other threads; it does not re-time the work after it. The earlier `steamcmd_block` bound (above, "≤ 0.24 % of the runs" against ±9.67 %) counts the runs removed only, the form this section finds can understate; it is not recomputed here, SteamCMD's records not having been downloaded again.
- `gdbus` threads of desktop services stay unknown; as desktop or unknown they are kept either way.

### Scripts

| script | what it does |
|---|---|
| `chain_roots.py` | census_core's tracing with each wake's way to its cause (direct, chain, relay, D-continuation) and root row kept; the check against census_core; the root groups |
| `effect_split.py` | `effect.py` with the shift under direct-only removal beside the rule's |
| `tally910.py` | the desktop sections' tracer with the scripted peers by their pid files, and the per-component tally with the split |
| `census_idle910.py` | `video-editor`'s idle repeats |
| `census_hidden910.py` | `renderer-hidden`'s steady repeats, per renderer |
| `census_launch910.py` | the ten launch phases, checked wake by wake against `dataset/launch`, with the reading from before the exec |
| `effect_launch910.py` | the launch streams' shifts per repeat and over the repeats |
| `census_bg910.py` | the seven background campaigns as `background/analyze.py` reads them, the values recomputed without the outside-cause wakes; `--session-by-package`, `--warm` |
| `effect_bg910.py` | the background check, counts by cause, class totals, bounds and recomputed shifts, the largest runs |
