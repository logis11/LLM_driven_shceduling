# Stability ledger — script output

Values on the stability lists of the records the library is folded from: **406**, over 28 entries (measured entries with no value on a list: none). 4 of them are the stimulus-sensitivity check's per-input means under 136M, on the lists but not carried (4 met the tolerance).

- Met the tolerance: **369** — of which 9 by the 1 µs floor rather than the 5 %, and 3 belong to a component carried under a class (its values together).
- Carried under 'Sparse component': **3**
- Carried under 'Varies between sessions': **15**
- Carried under 'Recording runs out': **10**
- Carried under 'Spread follows the machine': **9**
- 'Rare event within a run', beside the rule, not on a list: **2** events (web-browser `MemoryInfra`, 8 over 22,800 s, game-client `CHTTPClientThre`, 62 over 7,200 s)
- Unresolved (failing, no class, or under five repeats): **0**
- Records' pass flag against the rule re-derived from mean, half-width and count: 0 disagree
- Largest half-width carried: **61.28 %**, renderer-hidden `steady residual run mean (ms)` (Sparse component, 5 repeats)
- Largest half-width among the values that met the tolerance: 40.51 % (0.0646 µs), file-archiver `7z-mmt8-warm block per run (µs)`, by the 1 µs floor

## Per entry

| entry | values | met | Sparse component | Varies between sessions | Recording runs out | Spread follows the machine | widest half-width |
|---|---|---|---|---|---|---|---|
| office-writer | 5 | 5 |  |  |  |  | 4.96 % (`input_run mean, 136M (ms)`) |
| code-editor | 29 | 27 |  | 2 |  |  | 5.63 % (`idle utility/libuv-worker wakes/s`) |
| web-browser | 60 | 59 |  |  | 1 |  | 5.90 % (`input_run mean, SWELL-KW (ms)`) |
| mail-client | 84 | 75 |  |  | 9 |  | 18.42 % (`op StreamTrans run mean (ms)`) |
| image-editor | 10 | 10 |  |  |  |  | 4.40 % (`op script-fu run mean (ms)`) |
| video-editor | 22 | 22 |  |  |  |  | 5.00 % (`driven kdenlive run mean (ms)`) |
| audio-player | 3 | 3 |  |  |  |  | 4.68 % (`play CPU share`) |
| video-player | 3 | 3 |  |  |  |  | 2.86 % (`play CPU share`) |
| video-call | 3 | 3 |  |  |  |  | 1.52 % (`play CPU share`) |
| renderer-hidden | 18 | 4 | 3 | 9 |  | 2 | 61.28 % (`steady residual run mean (ms)`) |
| chat-client | 18 | 18 |  |  |  |  | 4.35 % (`idle residual run mean (ms)`) |
| game-client | 33 | 29 |  |  |  | 4 | 10.12 % (`shown steam run mean (ms)`) |
| compositor-shell | 9 | 9 |  |  |  |  | 2.82 % (`gnome-shell gnome-shell/gnome-shell run mean (ms)`) |
| audio-server | 3 | 3 |  |  |  |  | 4.48 % (`pipewire wireplumber/gmain wakes/s`) |
| service-manager | 3 | 2 |  | 1 |  |  | 7.77 % (`systemd pid1/systemd run mean (ms)`) |
| message-bus | 3 | 0 |  | 3 |  |  | 11.05 % (`dbus-daemon system-bus/dbus-daemon wakes/s`) |
| build-orchestrator | 1 | 1 |  |  |  |  | 0.94 % (`make dispatch`) |
| compiler-child | 17 | 17 |  |  |  |  | 2.00 % (`object-job sh 3/4`) |
| file-archiver | 2 | 2 |  |  |  |  | 40.51 % (`7z-mmt8-warm block per run (µs)`) |
| game-download, game-download-idle | 2 | 2 |  |  |  |  | 9.67 % (`steam-fresh-shaped block per run (µs)`) |
| package-upgrade | 3 | 3 |  |  |  |  | 5.97 % (`upgrade-install block per run (µs)`) |
| module-build-orchestrator | 4 | 3 |  |  |  | 1 | 8.35 % (`dkms-install tail block per run (µs)`) |
| module-compiler-child | 56 | 56 |  |  |  |  | 4.13 % (`dkms-install kprobe gcc step 2/3 (µs)`) |
| file-indexer | 3 | 3 |  |  |  |  | 3.58 % (`tracker-index block per run (µs)`) |
| cpu-batch (python3) | 3 | 1 |  |  |  | 2 | 27.31 % (`mnist-train run between voluntary blocks (µs)`) |
| cpu-batch (kdenlive_render) | 3 | 3 |  |  |  |  | 13.13 % (`kdenlive-export block per run (µs)`) |
| video-transcoder | 3 | 3 |  |  |  |  | 36.12 % (`handbrake-transcode block per run (µs)`) |
| incremental-backup | 3 | 3 |  |  |  |  | 6.19 % (`dejadup-incremental block per run (µs)`) |

## The values carried under a class

| class | entry | value | repeats | half-width | repeats the rule would need |
|---|---|---|---|---|---|
| Sparse component | renderer-hidden | `steady residual run mean (ms)` | 5 | 61.28 % | over 200 |
| Sparse component | renderer-hidden | `steady residual wakes/s` | 5 | 20.20 % | 44 |
| Sparse component | renderer-hidden | `steady residual gap mean (ms)` | 5 | 20.20 % | 44 |
| Varies between sessions | renderer-hidden | `steady Compositor wakes/s` | 5 | 17.56 % | 34 |
| Varies between sessions | renderer-hidden | `steady Compositor gap mean (ms)` | 5 | 17.56 % | 34 |
| Varies between sessions | renderer-hidden | `steady PerfettoTrace wakes/s` | 5 | 17.56 % | 34 |
| Varies between sessions | renderer-hidden | `steady PerfettoTrace gap mean (ms)` | 5 | 17.56 % | 34 |
| Varies between sessions | renderer-hidden | `steady Compositor run mean (ms)` | 5 | 12.28 % | 18 |
| Varies between sessions | message-bus | `dbus-daemon system-bus/dbus-daemon wakes/s` | 24 | 11.05 % | 108 |
| Varies between sessions | message-bus | `dbus-daemon system-bus/dbus-daemon gap mean (ms)` | 24 | 11.05 % | 108 |
| Varies between sessions | message-bus | `dbus-daemon system-bus/dbus-daemon run mean (ms)` | 24 | 10.74 % | 102 |
| Varies between sessions | renderer-hidden | `steady PerfettoTrace run mean (ms)` | 5 | 9.26 % | 12 |
| Varies between sessions | service-manager | `systemd pid1/systemd run mean (ms)` | 24 | 7.77 % | 55 |
| Varies between sessions | renderer-hidden | `steady Chrome_ChildIOT run mean (ms)` | 5 | 7.46 % | 9 |
| Varies between sessions | renderer-hidden | `steady Chrome_ChildIOT wakes/s` | 5 | 6.47 % | 7 |
| Varies between sessions | renderer-hidden | `steady Chrome_ChildIOT gap mean (ms)` | 5 | 6.47 % | 7 |
| Varies between sessions | code-editor | `idle utility/libuv-worker wakes/s` | 44 | 5.63 % | 56 |
| Varies between sessions | code-editor | `idle utility/libuv-worker gap mean (ms)` | 44 | 5.63 % | 56 |
| Recording runs out | mail-client | `op StreamTrans run mean (ms)` | 8 | 18.42 % | 78 |
| Recording runs out | mail-client | `op WRRende~ckend#0 run mean (ms)` | 8 | 11.15 % | 30 |
| Recording runs out | mail-client | `input_run mean, SWELL-KW (ms)` | 8 | 10.41 % | 27 |
| Recording runs out | mail-client | `op glean.dispatche run mean (ms)` | 8 | 8.18 % | 18 |
| Recording runs out | mail-client | `op residual run mean (ms)` | 8 | 6.59 % | 13 |
| Recording runs out | mail-client | `op StreamTrans gap mean (ms)` | 8 | 6.52 % | 12 |
| Recording runs out | mail-client | `op StreamTrans wakes/s` | 8 | 6.51 % | 12 |
| Recording runs out | web-browser | `input_run mean, SWELL-KW (ms)` | 38 | 5.90 % | 52 |
| Recording runs out | mail-client | `op Softwar~cThread run mean (ms)` | 8 | 5.45 % | 10 |
| Recording runs out | mail-client | `op Renderer run mean (ms)` | 8 | 5.37 % | 9 |
| Spread follows the machine | cpu-batch (python3) | `mnist-train run between voluntary blocks (µs)` | 6 | 27.31 % | 107 |
| Spread follows the machine | renderer-hidden | `steady HangWatcher run mean (ms)` | 5 | 18.08 % | 36 |
| Spread follows the machine | renderer-hidden | `steady chrome run mean (ms)` | 5 | 11.42 % | 16 |
| Spread follows the machine | cpu-batch (python3) | `mnist-train block per run (µs)` | 6 | 10.77 % | 19 |
| Spread follows the machine | game-client | `shown steam run mean (ms)` | 12 | 10.12 % | 42 |
| Spread follows the machine | game-client | `shown IPC:CSteamEngin run mean (ms)` | 12 | 8.78 % | 32 |
| Spread follows the machine | module-build-orchestrator | `dkms-install tail block per run (µs)` | 26 | 8.35 % | 69 |
| Spread follows the machine | game-client | `shown VizCompositorTh run mean (ms)` | 12 | 5.64 % | 15 |
| Spread follows the machine | game-client | `shown steamwebhelper run mean (ms)` | 12 | 5.27 % | 14 |

## Met by the 1 µs floor

| entry | value | repeats | half-width | absolute |
|---|---|---|---|---|
| file-archiver | `7z-mmt8-warm block per run (µs)` | 6 | 40.51 % | 0.0646 |
| video-transcoder | `handbrake-transcode block per run (µs)` | 5 | 36.12 % | 0.2187 |
| cpu-batch (kdenlive_render) | `kdenlive-export block per run (µs)` | 30 | 13.13 % | 0.6033 |
| game-download, game-download-idle | `steam-fresh-shaped block per run (µs)` | 30 | 9.67 % | 0.8995 |
| incremental-backup | `dejadup-incremental block per run (µs)` | 28 | 6.19 % | 0.231 |
| package-upgrade | `upgrade-install block per run (µs)` | 9 | 5.97 % | 0.5312 |
| game-client | `shown CJobMgr::m_Work run mean (ms)` | 12 | 5.69 % | 0.001 |
| mail-client | `op SwComposite run mean (ms)` | 8 | 5.38 % | 0.0007 |
| game-client | `shown ThreadPoolForeg run mean (ms)` | 12 | 5.07 % | 0.0009 |

## Held in the records, taken by no entry

| what | record | values |
|---|---|---|
| renderer-visible: not in the library | `_dev/research/jioh/task-9.8-browser-comms/campaign/results/pooled.json` | 15 |
| mail-client: the idle values of the record its other phases come from | `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-re-measured/pool-thunderbird-send.json` | 45 |
| mail-client: the other phases' values of its idle record | `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-thunderbird-send.json` | 39 |
| video-editor: the idle values of the record its other phases come from | `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-kdenlive.json` | 6 |
| renderer-hidden: 9.8's record, superseded | `_dev/research/jioh/task-9.8-browser-comms/campaign/results/pooled.json` | 21 |
| 9.6's retired cpu-batch programs (clamscan, ffmpeg, handbrake, train, tracker) | `_dev/research/jioh/task-9.6-compile/campaign/results/pooled.json` | 15 |

## Records read

- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/dejadup/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/dkms/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/handbrake/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/kdenlive-idle/results/pool-kdenlive.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/kdenlive/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/mnist/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/renderer-hidden/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/tracker/results/pooled.json`
- `_dev/research/jioh/task-9.10-scenarios-timelines/campaign/upgrade/results/pooled.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-re-measured/pool-chrome.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-re-measured/pool-code.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-re-measured/pool-thunderbird-send.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-re-measured/pool-webrtc.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-gimp.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-kdenlive.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-mpv-audio.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-mpv-video.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-soffice.json`
- `_dev/research/jioh/task-9.5-interactive-typing/campaign/results-same-machine/pool-thunderbird-send.json`
- `_dev/research/jioh/task-9.6-compile/campaign/results/pooled.json`
- `_dev/research/jioh/task-9.7-background-io/campaign/results/7z-pooled.json`
- `_dev/research/jioh/task-9.7-background-io/campaign/results/steamcmd-pooled.json`
- `_dev/research/jioh/task-9.8-browser-comms/campaign/results/pooled.json`
- `_dev/research/jioh/task-9.9-daemons-session/campaign/results/pooled.json`
