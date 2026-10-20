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
